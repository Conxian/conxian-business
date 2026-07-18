#!/usr/bin/env python3
"""Conxian Session Test Runner

Comprehensive test suite for agent sessions with reporting.

Usage:
    python3 scripts/session_test_runner.py --full      # Full test suite
    python3 scripts/session_test_runner.py --quick    # Quick health check
    python3 scripts/session_test_runner.py --report     # Generate report
    python3 scripts/session_test_runner.py --sync      # Sync to Linear
"""

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class TestResult:
    """Individual test result."""
    name: str
    passed: bool
    duration: float
    output: str = ""
    error: str = ""
    critical: bool = True


@dataclass
class SessionReport:
    """Complete session test report."""
    session_id: str
    start_time: str
    end_time: str
    duration: float
    tests_run: int
    tests_passed: int
    tests_failed: int
    critical_failures: int
    results: list
    git_status: dict = None
    recommendations: list = None


class SessionTester:
    """Session test runner with reporting."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: list[TestResult] = []
        self.start_time = datetime.now()
        self.session_id = f"SESSION-{self.start_time.strftime('%Y%m%d-%H%M%S')}"

    def run_command(self, cmd: str, timeout: int = 60) -> tuple[int, str, str]:
        """Run shell command and return (code, stdout, stderr)."""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=timeout, cwd=REPO_ROOT
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def run_test(self, name: str, command: str, critical: bool = True,
                 timeout: int = 60) -> TestResult:
        """Run a single test."""
        print(f"\n[TEST] {name}...", end=" ", flush=True)

        start = datetime.now()
        code, stdout, stderr = self.run_command(command, timeout)
        duration = (datetime.now() - start).total_seconds()

        passed = code == 0
        status = "✅ PASS" if passed else "❌ FAIL"
        print(status, f"({duration:.1f}s)")

        if self.verbose and stdout:
            for line in stdout.strip().split('\n')[:5]:
                print(f"    {line}")

        if not passed and stderr:
            print(f"    Error: {stderr[:100]}...")

        result = TestResult(
            name=name,
            passed=passed,
            duration=duration,
            output=stdout[:500],
            error=stderr[:500] if stderr else "",
            critical=critical
        )
        self.results.append(result)
        return result

    def get_git_status(self) -> dict:
        """Get git status summary."""
        code, stdout, _ = self.run_command("git status --short")
        if code == 0:
            lines = stdout.strip().split('\n') if stdout.strip() else []
            return {
                "modified": [l for l in lines if l.startswith('M ')],
                "added": [l for l in lines if l.startswith('A ')],
                "deleted": [l for l in lines if l.startswith('D ')],
                "untracked": [l for l in lines if l.startswith('?? ')],
            }
        return {}

    def run_integration_tests(self) -> list[TestResult]:
        """Run integration tests."""
        tests = [
            ("Market Integration", "python3 scripts/verify_market_integration.py", True, 60),
            ("MWP Test Suite", "python3 scripts/market_bos_mwp_test.py", True, 60),
        ]

        for name, cmd, critical, timeout in tests:
            self.run_test(name, cmd, critical, timeout)

        return self.results

    def run_assessment_tests(self) -> list[TestResult]:
        """Run assessment tests."""
        tests = [
            ("Submodule Integrity", "python3 scripts/verify_submodule_integrity.py", True, 30),
            ("Viability Assessment", "python3 scripts/repo_viability_assessment.py --all", False, 60),
            ("Contamination Guard", "python3 scripts/verify_contamination_guard.py", False, 30),
        ]

        for name, cmd, critical, timeout in tests:
            self.run_test(name, cmd, critical, timeout)

        return self.results

    def run_security_tests(self) -> list[TestResult]:
        """Run security tests."""
        tests = [
            ("Action Versions", "python3 scripts/verify_action_versions.py", False, 30),
            ("LTS Compliance", "python3 scripts/verify_lts_compliance.py", False, 30),
        ]

        for name, cmd, critical, timeout in tests:
            self.run_test(name, cmd, critical, timeout)

        return self.results

    def run_quick_tests(self) -> list[TestResult]:
        """Run quick health check."""
        tests = [
            ("Market Integration", "python3 scripts/verify_market_integration.py", True, 30),
            ("Git Status", "git status --short", True, 10),
        ]

        for name, cmd, critical, timeout in tests:
            self.run_test(name, cmd, critical, timeout)

        return self.results

    def print_summary(self) -> None:
        """Print test summary."""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        critical_failed = sum(1 for r in self.results if not r.passed and r.critical)
        total = len(self.results)

        duration = (datetime.now() - self.start_time).total_seconds()

        print("\n" + "="*60)
        print("  TEST SUMMARY")
        print("="*60)
        print(f"\nSession ID: {self.session_id}")
        print(f"Duration: {duration:.1f}s")
        print(f"\nResults: {passed}/{total} passed, {failed} failed")

        if critical_failed > 0:
            print(f"\n⚠️  {critical_failed} CRITICAL failures!")

        if failed > 0:
            print("\nFailed Tests:")
            for r in self.results:
                if not r.passed:
                    icon = "🔴" if r.critical else "🟡"
                    print(f"  {icon} {r.name}")
                    if r.error:
                        print(f"      {r.error[:80]}...")

        print("\n" + "="*60)

        # Recommendations
        if critical_failed > 0:
            print("\n📋 RECOMMENDATIONS:")
            print("  1. Fix critical failures before committing")
            print("  2. Run --full suite for complete verification")
            print("  3. Update BOS_KNOWLEDGE_GRAPH.md with findings")

    def generate_report(self) -> SessionReport:
        """Generate session report."""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        critical_failed = sum(1 for r in self.results if not r.passed and r.critical)
        duration = (datetime.now() - self.start_time).total_seconds()

        recommendations = []
        if critical_failed > 0:
            recommendations.append("Fix critical test failures before proceeding")
        if failed > 0:
            recommendations.append("Review non-critical failures in next sprint")
        if not any(r.name == "Viability Assessment" and r.passed for r in self.results):
            recommendations.append("Run full viability assessment weekly")

        return SessionReport(
            session_id=self.session_id,
            start_time=self.start_time.isoformat(),
            end_time=datetime.now().isoformat(),
            duration=duration,
            tests_run=len(self.results),
            tests_passed=passed,
            tests_failed=failed,
            critical_failures=critical_failed,
            results=[asdict(r) for r in self.results],
            git_status=self.get_git_status(),
            recommendations=recommendations
        )

    def save_report(self, format: str = "json") -> Path:
        """Save test report to file."""
        report = self.generate_report()

        if format == "json":
            path = REPO_ROOT / f"session-report-{self.session_id}.json"
            with open(path, 'w') as f:
                json.dump(asdict(report), f, indent=2)
        else:
            path = REPO_ROOT / f"session-report-{self.session_id}.md"
            with open(path, 'w') as f:
                f.write(f"# Session Test Report: {self.session_id}\n\n")
                f.write(f"**Date**: {report.start_time}\n\n")
                f.write(f"## Summary\n\n")
                f.write(f"| Metric | Value |\n")
                f.write(f"|--------|-------|\n")
                f.write(f"| Duration | {report.duration:.1f}s |\n")
                f.write(f"| Tests | {report.tests_run} |\n")
                f.write(f"| Passed | {report.tests_passed} |\n")
                f.write(f"| Failed | {report.tests_failed} |\n")
                f.write(f"| Critical | {report.critical_failures} |\n\n")

                f.write(f"## Results\n\n")
                for r in report.results:
                    status = "✅" if r["passed"] else "❌"
                    f.write(f"| {status} | {r['name']} | {r['duration']:.1f}s |\n")

        return path


def main():
    parser = argparse.ArgumentParser(description="Conxian Session Test Runner")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    parser.add_argument("--quick", action="store_true", help="Quick health check")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    tester = SessionTester(verbose=args.verbose)

    print("="*60)
    print("  CONXIAN SESSION TEST RUNNER")
    print("="*60)
    print(f"Session: {tester.session_id}")
    print(f"Started: {tester.start_time.isoformat()}\n")

    # Run appropriate tests
    if args.quick:
        print("Running QUICK health check...\n")
        tester.run_quick_tests()
    elif args.integration:
        print("Running INTEGRATION tests...\n")
        tester.run_integration_tests()
    elif args.security:
        print("Running SECURITY tests...\n")
        tester.run_security_tests()
    elif args.full:
        print("Running FULL test suite...\n")
        tester.run_integration_tests()
        tester.run_assessment_tests()
        tester.run_security_tests()
    else:
        print("Running DEFAULT tests...\n")
        tester.run_integration_tests()
        tester.run_assessment_tests()

    # Print summary
    tester.print_summary()

    # Generate report if requested
    if args.report:
        path = tester.save_report(format=args.format)
        print(f"\n📄 Report saved to: {path}")

    # Exit with appropriate code
    critical_failures = sum(1 for r in tester.results if not r.passed and r.critical)
    sys.exit(0 if critical_failures == 0 else 1)


if __name__ == "__main__":
    main()
