let addRowCallCounter = 1;

function addRow(productName, unit, pricePerUnit) {
  var tableBody = document.querySelector(".table-responsive table tbody");

  if (!tableBody) {
    tableBody = document.createElement("tbody");
    document.querySelector(".table-responsive table").appendChild(tableBody);
  }

  var newRow = document.createElement("tr");
  newRow.innerHTML = `
      <td>${productName}</td>
      <td><input class="form-control txtLabel" name="txtB${addRowCallCounter}" readonly size="5" type="text" value="0.00" /></td>
      <td>${unit}</td>
      <td><input class="form-control txtLabel" name="txtC${addRowCallCounter}" readonly size="6" type="text" value="${pricePerUnit}" /></td>
      <td><input class="form-control txtLabel" name="txtD${addRowCallCounter}" readonly size="8" type="text" value="0.00" /></td>
      `;

  tableBody.appendChild(newRow);
  addRowCallCounter++;
}

function addSummaryRows() {
  const tableBody = document.querySelector(".table-responsive table tbody");

  if (!tableBody) return; // If there is no table body, return

  const summaryRows = `
    <tr>
      <td colspan="3"></td>
      <th>SUBTOTAL</th>
      <td class="text-center">
          <input
              class="form-control-plaintext"
              id="txtB37"
              name="txtSub"
              readonly
              type="text"
              value="0.00"
          />
      </td>
    </tr>
    <tr>
      <td colspan="3"></td>
      <th>
          <span class="listado_precios">IVA (16%)</span>
      </th>
      <td class="text-center">
          <input
              class="form-control-plaintext"
              id="txtB38"
              name="txtIVA"
              readonly
              type="text"
              value="0.00"
          />
      </td>
    </tr>
    <tr>
      <td colspan="3"></td>
      <th>Total</th>
      <th class="text-center">
          <input
              class="form-control-plaintext"
              id="txtB39"
              name="txtTOT"
              readonly
              type="text"
              value="0.00"
          />
      </th>
    </tr>
  `;

  tableBody.innerHTML += summaryRows; // Append the summary rows to the table body
}



function addAllRows() {
  addRow("&Aacute;ngulo De Amarre 3mts Cal.26", "Pza.", 34.0);
  addRow("Canaleta de Carga 1 1/2&quot; x 3mts Cal.22", "Pza.", 79.0);
  addRow("Redimix Pasta Tablaroca 21.8 kg", "Caja", 299.0);
  addRow("Perfacinta (USA) 75mts", "Rollo", 78.0);
  addRow("Canal Liston 7/8&quot; x 3mts Cal.26", "Pza.", 45.0);
  addRow("Tablaroca Ultralight 1/2&quot;", "Pza.", 172.0);
  addRow("Tornillo 1&quot; Fina", "Pza.", 0.2);
  addRow("Tornillo Mini 1/2&quot; PN", "Pza.", 0.2);
  addRow("Alambre Cal.18", "Kg.", 58.0);
  addRow("Alambre Cal. 14", "Kg.", 58.0);
  addRow("Clavo p/ Concreto 1&quot;", "kg.", 82.0);
  addRow("Clavo Con Ancla 1&quot;", "Pza.", 4.5);
}

window.onload = function () {
  addAllRows();
  addSummaryRows();   
};
