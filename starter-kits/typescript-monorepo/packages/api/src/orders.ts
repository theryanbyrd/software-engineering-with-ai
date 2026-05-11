import { formatUsd, ok, err, type Result } from "@starter/shared";

export type CreateOrderInput = {
  amountCents: number;
  customerId: string;
};

export type Order = {
  id: string;
  amountCents: number;
  customerId: string;
  formattedAmount: string;
  createdAt: Date;
};

let counter = 0;

/**
 * Create an order. Validates inputs at the boundary.
 *
 * Returns a Result rather than throwing for expected validation failures.
 * Throws only for unexpected programmer errors.
 */
export function createOrder(input: CreateOrderInput): Result<Order, string> {
  if (!Number.isInteger(input.amountCents)) {
    return err("amountCents must be an integer (cents)");
  }
  if (input.amountCents < 0) {
    return err("amountCents must be non-negative");
  }
  if (!input.customerId || input.customerId.trim().length === 0) {
    return err("customerId is required");
  }

  counter += 1;
  const order: Order = {
    id: `ord_${Date.now()}_${counter}`,
    amountCents: input.amountCents,
    customerId: input.customerId,
    formattedAmount: formatUsd(input.amountCents),
    createdAt: new Date(),
  };
  return ok(order);
}
