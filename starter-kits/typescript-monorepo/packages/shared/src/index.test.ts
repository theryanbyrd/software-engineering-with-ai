import { describe, it, expect } from "vitest";
import { formatUsd, ok, err } from "./index.js";

describe("formatUsd", () => {
  it("formats whole dollars", () => {
    expect(formatUsd(10000)).toBe("$100.00");
  });

  it("formats with cents", () => {
    expect(formatUsd(12345)).toBe("$123.45");
  });

  it("formats single-digit cents with leading zero", () => {
    expect(formatUsd(105)).toBe("$1.05");
  });

  it("formats zero", () => {
    expect(formatUsd(0)).toBe("$0.00");
  });

  it("formats negative amounts with leading minus", () => {
    expect(formatUsd(-12345)).toBe("-$123.45");
  });

  it("throws on non-integer input", () => {
    expect(() => formatUsd(99.5)).toThrow(/integer/);
  });
});

describe("Result helpers", () => {
  it("ok wraps a value", () => {
    const r = ok(42);
    expect(r.ok).toBe(true);
    if (r.ok) expect(r.value).toBe(42);
  });

  it("err wraps an error", () => {
    const r = err("boom");
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error).toBe("boom");
  });
});
