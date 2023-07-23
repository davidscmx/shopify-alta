// Function to add a new row to the "Artículos" table
let addRowCallCounter = 1;

function addRow(item, unit, priceUnit) {
  const tableBody = document
    .getElementById("articulosTable")
    .getElementsByTagName("tbody")[0];
  const newRow = document.createElement("tr");
  newRow.innerHTML = `
    <tr>
    <td class="bg-white text-left txt_caracteristicas_relleno">${item}</td>
    <td class="bg-light text-center txt_caracteristicas_relleno">
      <input class="form-control txtLabel" name="txtB${addRowCallCounter}" readonly size="5" type="text" value="0" />
    </td>
    <td class="bg-light text-center txt_caracteristicas_relleno">${unit}</td>
    <td class="bg-light text-center txt_caracteristicas_relleno">
      <input class="form-control txtLabel" name="txtC${addRowCallCounter}" readonly size="6" type="text" value=$${priceUnit} />
    </td>
    <td class="bg-light text-center txt_caracteristicas_relleno">
      <input class="form-control txtLabel" name="txtD${addRowCallCounter}" readonly size="6" type="text" value="0.0" />
    </td>
  </tr>
    `;
  addRowCallCounter++;
  tableBody.appendChild(newRow);
}
