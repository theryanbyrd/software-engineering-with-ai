import { describe, it, expect } from "vitest";
import { createOrder } from "../src/orders.js";

describe("createOrder", () => {
  it("returns an ok result with a formatted order when input is valid", () => {
    const result = createOrder({ amountCents: 12345, customerId: "cust_1" });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.value.amountCents).toBe(12345);
      expect(result.value.formattedAmount).toBe("$123.45");
      expect(result.value.customerId).toBe("cust_1");
      expect(result.value.id).toMatch(/^ord_/);
    }
  });

  it("rejects non-integer amounts", () => {
    const result = createOrder({ amountCents: 99.5, customerId: "cust_1" });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toMatch(/integer/);
    }
  });

  it("rejects negative amounts", () => {
    const result = createOrder({ amountCents: -1, customerId: "cust_1" });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toMatch(/non-negative/);
    }
  });

  it("rejects empty customerId", () => {
    const result = createOrder({ amountCents: 100, customerId: "" });
    expect(result.ok).toBe(false);
  });

  it("rejects whitespace-only customerId", () => {
    const result = createOrder({ amountCents: 100, customerId: "   " });
    expect(result.ok).toBe(false);
  });
});
