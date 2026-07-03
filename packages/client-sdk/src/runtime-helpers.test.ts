import { beforeEach, describe, expect, it } from "bun:test";
import {
  AdminRuntimeConfigError,
  buildEndpointUrl,
  buildHeaders,
  configureAdminRuntimeClient,
  normalizeRuntimeBaseUrl,
  parseRuntimeErrorEnvelope,
  resetAdminRuntimeClientConfig,
  resolveFetchImplementation,
  resolveRuntimeBaseUrl,
} from "./runtime-client";

describe("normalizeRuntimeBaseUrl", () => {
  it("strips trailing slashes", () => {
    expect(normalizeRuntimeBaseUrl("https://runtime.internal/")).toBe("https://runtime.internal");
  });

  it("strips multiple trailing slashes", () => {
    expect(normalizeRuntimeBaseUrl("https://runtime.internal////")).toBe("https://runtime.internal");
  });

  it("preserves URL with no trailing slash", () => {
    expect(normalizeRuntimeBaseUrl("https://runtime.internal")).toBe("https://runtime.internal");
  });

  it("handles URL with path and no trailing slash", () => {
    expect(normalizeRuntimeBaseUrl("https://runtime.internal/api/v2")).toBe("https://runtime.internal/api/v2");
  });

  it("strips trailing slashes from URL with path", () => {
    expect(normalizeRuntimeBaseUrl("https://runtime.internal/api/v2///")).toBe("https://runtime.internal/api/v2");
  });
});

describe("buildEndpointUrl", () => {
  const base = "https://runtime.internal";

  it("joins base with path that has a leading slash", () => {
    expect(buildEndpointUrl("/admin/v1/health", base)).toBe("https://runtime.internal/admin/v1/health");
  });

  it("joins base with path that has no leading slash", () => {
    expect(buildEndpointUrl("admin/v1/health", base)).toBe("https://runtime.internal/admin/v1/health");
  });

  it("preserves query strings", () => {
    expect(buildEndpointUrl("/admin/v1/search?q=test", base)).toBe("https://runtime.internal/admin/v1/search?q=test");
  });

  it("handles root path correctly", () => {
    expect(buildEndpointUrl("/", base)).toBe("https://runtime.internal/");
  });

  it("handles empty path correctly", () => {
    expect(buildEndpointUrl("", base)).toBe("https://runtime.internal/");
  });
});

describe("buildHeaders", () => {
  beforeEach(() => {
    resetAdminRuntimeClientConfig();
  });

  it("returns empty headers when no config or args are provided", () => {
    const headers = buildHeaders();
    expect([...headers.entries()]).toEqual([]);
  });

  it("includes default headers from runtime config", () => {
    configureAdminRuntimeClient({
      defaultHeaders: { "x-custom": "default-value" },
    });

    const headers = buildHeaders();
    expect(headers.get("x-custom")).toBe("default-value");
  });

  it("merges init headers on top of defaults", () => {
    configureAdminRuntimeClient({
      defaultHeaders: { "x-default": "a", "x-shared": "from-default" },
    });

    const headers = buildHeaders({ "x-init": "b", "x-shared": "from-init" });
    expect(headers.get("x-default")).toBe("a");
    expect(headers.get("x-init")).toBe("b");
    expect(headers.get("x-shared")).toBe("from-init");
  });

  it("merges options headers with highest priority", () => {
    configureAdminRuntimeClient({
      defaultHeaders: { "x-default": "a", "x-shared": "from-default" },
    });

    const headers = buildHeaders(
      { "x-init": "b", "x-shared": "from-init" },
      { "x-opt": "c", "x-shared": "from-opt" },
    );

    expect(headers.get("x-default")).toBe("a");
    expect(headers.get("x-init")).toBe("b");
    expect(headers.get("x-opt")).toBe("c");
    expect(headers.get("x-shared")).toBe("from-opt");
  });
});

describe("parseRuntimeErrorEnvelope", () => {
  it("returns undefined for non-JSON content-type", async () => {
    const response = new Response("plain text", {
      headers: { "content-type": "text/plain" },
      status: 500,
    });

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toBeUndefined();
  });

  it("returns undefined when content-type header is missing", async () => {
    const response = new Response("{}");

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toBeUndefined();
  });

  it("parses a valid error envelope", async () => {
    const response = new Response(
      JSON.stringify({
        error: { code: "TIMEOUT", message: "Request timed out", traceId: "abc123" },
      }),
      {
        headers: { "content-type": "application/json" },
        status: 504,
      },
    );

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toEqual({
      code: "TIMEOUT",
      message: "Request timed out",
      traceId: "abc123",
    });
  });

  it("returns undefined for JSON without error key", async () => {
    const response = new Response(JSON.stringify({ status: "ok" }), {
      headers: { "content-type": "application/json" },
      status: 200,
    });

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toBeUndefined();
  });

  it("returns undefined for JSON with invalid error shape", async () => {
    const response = new Response(
      JSON.stringify({ error: { description: "no code or message" } }),
      {
        headers: { "content-type": "application/json" },
        status: 500,
      },
    );

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toBeUndefined();
  });

  it("returns undefined for malformed JSON", async () => {
    const response = new Response("{not valid json", {
      headers: { "content-type": "application/json" },
      status: 500,
    });

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toBeUndefined();
  });

  it("handles error envelope with missing traceId", async () => {
    const response = new Response(
      JSON.stringify({
        error: { code: "FORBIDDEN", message: "Access denied" },
      }),
      {
        headers: { "content-type": "application/json" },
        status: 403,
      },
    );

    const result = await parseRuntimeErrorEnvelope(response);
    expect(result).toEqual({
      code: "FORBIDDEN",
      message: "Access denied",
    });
  });
});

describe("resolveRuntimeBaseUrl", () => {
  beforeEach(() => {
    resetAdminRuntimeClientConfig();
  });

  it("throws AdminRuntimeConfigError when no base URL is configured", () => {
    expect(() => resolveRuntimeBaseUrl()).toThrow(AdminRuntimeConfigError);
  });

  it("uses runtimeBaseUrl from options", () => {
    const url = resolveRuntimeBaseUrl({ runtimeBaseUrl: "https://custom.internal/" });
    expect(url).toBe("https://custom.internal");
  });

  it("uses runtimeBaseUrl from global config", () => {
    configureAdminRuntimeClient({ runtimeBaseUrl: "https://global.internal/" });
    const url = resolveRuntimeBaseUrl();
    expect(url).toBe("https://global.internal");
  });

  it("prefers options over global config", () => {
    configureAdminRuntimeClient({ runtimeBaseUrl: "https://global.internal/" });
    const url = resolveRuntimeBaseUrl({ runtimeBaseUrl: "https://options.internal/" });
    expect(url).toBe("https://options.internal");
  });

  it("throws for whitespace-only URL in options", () => {
    expect(() => resolveRuntimeBaseUrl({ runtimeBaseUrl: "   " })).toThrow(AdminRuntimeConfigError);
  });

  it("throws for empty string URL in config", () => {
    configureAdminRuntimeClient({ runtimeBaseUrl: "" });
    expect(() => resolveRuntimeBaseUrl()).toThrow(AdminRuntimeConfigError);
  });

  it("normalizes trailing slashes from resolved URL", () => {
    configureAdminRuntimeClient({ runtimeBaseUrl: "https://runtime.internal///" });
    const url = resolveRuntimeBaseUrl();
    expect(url).toBe("https://runtime.internal");
  });
});

describe("resolveFetchImplementation", () => {
  beforeEach(() => {
    resetAdminRuntimeClientConfig();
  });

  it("returns globalThis.fetch when nothing is configured", () => {
    const fetchImpl = resolveFetchImplementation();
    expect(fetchImpl).toBe(globalThis.fetch);
  });

  it("uses fetchImpl from options", () => {
    const customFetch = async () => new Response("ok");
    const fetchImpl = resolveFetchImplementation({ fetchImpl: customFetch });
    expect(fetchImpl).toBe(customFetch);
  });

  it("uses fetchImpl from global config", () => {
    const customFetch = async () => new Response("ok");
    configureAdminRuntimeClient({ fetchImpl: customFetch });
    const fetchImpl = resolveFetchImplementation();
    expect(fetchImpl).toBe(customFetch);
  });

  it("prefers options fetchImpl over global config", () => {
    const globalFetch = async () => new Response("global");
    const optionsFetch = async () => new Response("options");
    configureAdminRuntimeClient({ fetchImpl: globalFetch });
    const fetchImpl = resolveFetchImplementation({ fetchImpl: optionsFetch });
    expect(fetchImpl).toBe(optionsFetch);
  });

  it("throws AdminRuntimeConfigError when globalThis.fetch is not a function", () => {
    const originalFetch = globalThis.fetch;
    try {
      // @ts-expect-error simulate missing fetch
      delete (globalThis as Record<string, unknown>).fetch;
      expect(() => resolveFetchImplementation()).toThrow(AdminRuntimeConfigError);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });
});
