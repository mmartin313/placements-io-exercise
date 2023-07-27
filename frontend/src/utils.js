export const toUSD = (input) => {
  let USDollar = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    roundingMode: "ceil",
  });
  return USDollar.format(input);
};

export const toEUR = (input) => {
  let Euro = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "EUR",
    roundingMode: "ceil",
  });
  return Euro.format(input);
};
