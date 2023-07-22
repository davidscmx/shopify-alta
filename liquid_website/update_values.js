function removeNonNumbersAndParseFloat(inputString) {
  console.log("inputString "+inputString)
  const numericString = inputString.replace(/[^\d.]/g, ''); // Remove non-numeric characters
  console.log("numeric "+numericString)
  const floatValue = parseFloat(numericString); // Convert the numeric string to an integer
  console.log("resulting float "+floatValue)
  return floatValue;
}

function updateValues() {
    const tf = document.plafon;
    let width = parseFloat(tf.txtAncho.value); // D12
    let length = parseFloat(tf.txtLargo.value); // D10

    tf.txtLargo.value = length+" m";
    tf.txtAncho.value = width+" m";
    const area = width * length;
    tf.txtArea.value = area;

    // Quantities
    const calculateCeil = (value) => Math.ceil(value);

    tf.txtB1.value = calculateCeil((2 * (width + length)) / 3);
    tf.txtB2.value = calculateCeil(area * 0.28);
    tf.txtB3.value = calculateCeil(area / 28);
    tf.txtB4.value = calculateCeil(area * 0.02);
    tf.txtB5.value = calculateCeil((Math.floor(length / 0.61) * width) / 3);
    tf.txtB6.value = calculateCeil(area / 3);
    tf.txtB7.value = calculateCeil((30 * tf.txtB6.value) / 100) * 100;
    tf.txtB8.value = calculateCeil((area / 3)* 10) ;
    tf.txtB9.value = calculateCeil(area / 50);
    tf.txtB10.value = calculateCeil(area / 33);
    tf.txtB11.value = (area / 127).toFixed(2);
    tf.txtB12.value = calculateCeil(area * 0.7);

    tf.txtArea.value = tf.txtArea.value+" m\u00B2";

    // Totals
    const calculateTotal = (txtBValue, txtCValue) =>
      (parseFloat(txtBValue) * parseFloat(txtCValue)).toFixed(2);


    tf.txtD1.value = calculateTotal(tf.txtB1.value, removeNonNumbersAndParseFloat(tf.txtC1.value));
    tf.txtD2.value = calculateTotal(tf.txtB2.value, removeNonNumbersAndParseFloat(tf.txtC2.value));
    tf.txtD3.value = calculateTotal(tf.txtB3.value, removeNonNumbersAndParseFloat(tf.txtC3.value));
    tf.txtD4.value = calculateTotal(tf.txtB4.value, removeNonNumbersAndParseFloat(tf.txtC4.value));
    tf.txtD5.value = calculateTotal(tf.txtB5.value, removeNonNumbersAndParseFloat(tf.txtC5.value));
    tf.txtD6.value = calculateTotal(tf.txtB6.value, removeNonNumbersAndParseFloat(tf.txtC6.value));
    tf.txtD7.value = calculateTotal(tf.txtB7.value, removeNonNumbersAndParseFloat(tf.txtC7.value));
    tf.txtD8.value = calculateTotal(tf.txtB8.value, removeNonNumbersAndParseFloat(tf.txtC8.value));
    tf.txtD9.value = calculateTotal(tf.txtB9.value, removeNonNumbersAndParseFloat(tf.txtC9.value));
    tf.txtD10.value = calculateTotal(tf.txtB10.value, removeNonNumbersAndParseFloat(tf.txtC10.value));
    tf.txtD11.value = calculateTotal(tf.txtB11.value, removeNonNumbersAndParseFloat(tf.txtC11.value));
    tf.txtD12.value = calculateTotal(tf.txtB12.value, removeNonNumbersAndParseFloat(tf.txtC12.value));

    // Finalize operations
    const calculateSum = (values) =>
      values.reduce((acc, val) => acc + parseFloat(val), 0).toFixed(2);

    tf.txtSub.value = calculateSum([
      tf.txtD1.value,
      tf.txtD2.value,
      tf.txtD3.value,
      tf.txtD4.value,
      tf.txtD5.value,
      tf.txtD6.value,
      tf.txtD7.value,
      tf.txtD8.value,
      tf.txtD9.value,
      tf.txtD10.value,
      tf.txtD11.value,
      tf.txtD12.value,
    ]);
    tf.txtIVA.value = (tf.txtSub.value * 0.16).toFixed(2);
    tf.txtTOT.value = (parseFloat(tf.txtSub.value) + parseFloat(tf.txtIVA.value)).toFixed(2);

    tf.txtSub.value = "$"+tf.txtSub.value
    tf.txtTOT.value = "$"+tf.txtTOT.value
    tf.txtIVA.value = "$"+tf.txtIVA.value

    // add pesos sign to total price of product
    tf.txtD1.value = "$"+tf.txtD1.value;
    tf.txtD2.value = "$"+tf.txtD2.value;
    tf.txtD3.value = "$"+tf.txtD3.value;
    tf.txtD4.value = "$"+tf.txtD4.value;
    tf.txtD5.value = "$"+tf.txtD5.value;
    tf.txtD6.value = "$"+tf.txtD6.value;
    tf.txtD7.value = "$"+tf.txtD7.value;
    tf.txtD8.value = "$"+tf.txtD8.value;
    tf.txtD9.value = "$"+tf.txtD9.value;
    tf.txtD10.value = "$"+tf.txtD10.value;
    tf.txtD11.value = "$"+tf.txtD11.value;
    tf.txtD12.value = "$"+tf.txtD12.value;
  }
