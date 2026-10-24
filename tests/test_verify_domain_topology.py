import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("topology", Path(__file__).resolve().parents[1] / "scripts/verify_domain_topology.py")
topology = importlib.util.module_from_spec(spec)
spec.loader.exec_module(topology)


def healthy_surface(url):
    if url.endswith("/api/health"):
        return 200, "application/json; charset=utf-8", json.dumps({"status": "healthy"})
    return 200, "text/html", "<title>Conxian BOS Control Plane</title>"


class TopologyReadinessTests(unittest.TestCase):
    def test_qualified_surfaces(self):
        self.assertEqual(topology.check_urls(lambda _: 200, healthy_surface), [])

    def test_successful_homepages_do_not_hide_backend_failure(self):
        def unavailable(url):
            if url.endswith("/api/health"):
                return 503, "application/json", '{"status":"unhealthy"}'
            return healthy_surface(url)
        self.assertEqual(len(topology.check_urls(lambda _: 200, unavailable)), 2)

    def test_login_or_fallback_html_is_not_json_readiness(self):
        for response in [(200, "text/html", "<title>Sign in</title>"),
                         (200, "application/json", "null"),
                         (200, "application/json", "{bad"),
                         (200, "application/json", '{"status":"unknown"}'),
                         (200, "application/json", '{"status":true}')]:
            with self.subTest(response=response):
                errors = topology.check_urls(lambda _: 200,
                    lambda url: response if url.endswith("/api/health") else healthy_surface(url))
                self.assertEqual(len(errors), 2)

    def test_wrong_application_on_control_domain_is_not_healthy(self):
        errors = topology.check_urls(lambda _: 200,
            lambda url: healthy_surface(url) if url.endswith("/api/health") else
            (200, "text/html", "<title>Conxian Platform | Operations</title>"))
        self.assertEqual(errors, ["control.conxian-labs.com: BOS control application identity not established"])

    def test_network_errors_are_sanitized(self):
        def broken(_):
            raise OSError("private connection details")
        errors = topology.check_urls(lambda _: 200, broken)
        self.assertEqual(len(errors), 3)
        self.assertNotIn("private", str(errors))

    def test_missing_dns_cannot_report_full_alignment(self):
        with patch.dict(topology.os.environ, {}, clear=True), patch.object(topology, "check_urls", return_value=[]):
            self.assertEqual(topology.main([]), 1)
            self.assertEqual(topology.main(["--http-only"]), 0)

    def test_readiness_rejects_cross_origin_redirects(self):
        request = topology.urllib.request.Request("https://control.conxian-labs.com/api/health")
        with self.assertRaisesRegex(ValueError, "cross-origin"):
            topology.SameOriginRedirect().redirect_request(request, None, 302, "", {}, "https://other.example/login")


if __name__ == "__main__":
    unittest.main()
