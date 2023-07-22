// Function to add a new row to the "Artículos" table
let addRowCallCounter = 1;

function addRow(item, unit, priceUnit) {
    const tableBody = document.getElementById("articulosTable").getElementsByTagName('tbody')[0];
    const newRow = document.createElement("tr");
    newRow.innerHTML = `
      <td bgcolor="#FFFFFF" class="txt_caracteristicas_relleno">
        <div align="left">${item}</div>
      </td>
      <td align="center" bgcolor="#CCCCCC" class="txt_caracteristicas_relleno">
        <input class="txtLabel" name="txtB${addRowCallCounter}" readonly="readonly" size="5" type="text" value="0" />
      </td>
      <td align="center" bgcolor="#CCCCCC" class="txt_caracteristicas_relleno">${unit}</td>
      <td align="center" bgcolor="#CCCCCC" class="txt_caracteristicas_relleno">
       <input class="txtLabel" name="txtC${addRowCallCounter}" readonly="readonly" size="6" type="text" value=$${priceUnit} />
      </td>
      <td align="center" bgcolor="#CCCCCC" class="txt_caracteristicas_relleno">
        <input class="txtLabel" name="txtD${addRowCallCounter}" readonly="readonly" size="6" type="text" value="0.0" />
      </td>
    `;
    addRowCallCounter++;
    tableBody.appendChild(newRow);
  }
