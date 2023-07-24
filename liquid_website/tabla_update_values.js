function removeNonNumbersAndParseFloat(inputString) {
  const numericString = inputString.replace(/[^\d.]/g, ""); // Remove non-numeric characters
  const floatValue = parseFloat(numericString); // Convert the numeric string to a float
  return floatValue;
}

function updateValues() {
  let width = parseFloat(document.getElementsByName("txtAncho")[0].value);
  let length = parseFloat(document.getElementsByName("txtLargo")[0].value);

  document.getElementsByName("txtLargo")[0].value = length + " m";
  document.getElementsByName("txtAncho")[0].value = width + " m";
  const area = width * length;
  document.getElementsByName("txtArea")[0].value = area;

  // Quantities
  const calculateCeil = (value) => Math.ceil(value);

  document.getElementsByName("txtB1")[0].value = calculateCeil(
    (2 * (width + length)) / 3
  );
  document.getElementsByName("txtB2")[0].value = calculateCeil(area * 0.28);
  document.getElementsByName("txtB3")[0].value = calculateCeil(area / 28);
  document.getElementsByName("txtB4")[0].value = calculateCeil(area * 0.02);
  document.getElementsByName("txtB5")[0].value = calculateCeil(
    (Math.floor(length / 0.61) * width) / 3
  );
  document.getElementsByName("txtB6")[0].value = calculateCeil(area / 3);
  document.getElementsByName("txtB7")[0].value =
    calculateCeil((30 * document.getElementsByName("txtB6")[0].value) / 100) *
    100;
  document.getElementsByName("txtB8")[0].value = calculateCeil((area / 3) * 10);
  document.getElementsByName("txtB9")[0].value = calculateCeil(area / 50);
  document.getElementsByName("txtB10")[0].value = calculateCeil(area / 33);
  document.getElementsByName("txtB11")[0].value = (area / 127).toFixed(2);
  document.getElementsByName("txtB12")[0].value = calculateCeil(area * 0.7);

  document.getElementsByName("txtArea")[0].value =
    document.getElementsByName("txtArea")[0].value + " m\u00B2";

  // Totals
  const calculateTotal = (txtBValue, txtCValue) =>
    (parseFloat(txtBValue) * parseFloat(txtCValue)).toFixed(2);

  for (let i = 1; i <= 12; i++) {
    document.getElementsByName(`txtD${i}`)[0].value = calculateTotal(
      document.getElementsByName(`txtB${i}`)[0].value,
      document.getElementsByName(`txtC${i}`)[0].value
    );
  }

  // Finalize operations
  const calculateSum = (values) =>
    values.reduce((acc, val) => acc + parseFloat(val), 0).toFixed(2);

  const dValues = Array.from(
    { length: 12 },
    (_, i) => document.getElementsByName(`txtD${i + 1}`)[0].value
  );
  document.getElementsByName("txtSub")[0].value = calculateSum(dValues);
  document.getElementsByName("txtIVA")[0].value = (
    document.getElementsByName("txtSub")[0].value * 0.16
  ).toFixed(2);
  document.getElementsByName("txtTOT")[0].value = (
    parseFloat(document.getElementsByName("txtSub")[0].value) +
    parseFloat(document.getElementsByName("txtIVA")[0].value)
  ).toFixed(2);

  document.getElementsByName("txtSub")[0].value =
    "$" + document.getElementsByName("txtSub")[0].value;
  document.getElementsByName("txtTOT")[0].value =
    "$" + document.getElementsByName("txtTOT")[0].value;
  document.getElementsByName("txtIVA")[0].value =
    "$" + document.getElementsByName("txtIVA")[0].value;

  // add pesos sign to total price of product
  for (let i = 1; i <= 12; i++) {
    document.getElementsByName(`txtD${i}`)[0].value =
      "$" + document.getElementsByName(`txtD${i}`)[0].value;
  }
}

document.querySelector("#plafon").addEventListener("submit", updateValues);
