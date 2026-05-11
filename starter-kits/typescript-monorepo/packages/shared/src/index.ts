/**
 * Format an integer cents value as a USD currency string.
 *
 * @param cents - Amount in integer cents (e.g., 12345 for $123.45).
 * @returns Formatted string with two decimal places and a leading $.
 * @throws if `cents` is not an integer.
 */
export function formatUsd(cents: number): string {
  if (!Number.isInteger(cents)) {
    throw new Error("amount must be an integer (cents)");
  }
  const sign = cents < 0 ? "-" : "";
  const abs = Math.abs(cents);
  const dollars = Math.floor(abs / 100);
  const remainder = abs % 100;
  return `${sign}$${dollars}.${remainder.toString().padStart(2, "0")}`;
}

/**
 * Result of a fallible operation. Functional style — no exceptions for expected failures.
 */
export type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

export function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}
