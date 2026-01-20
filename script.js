let bleCharacteristic = null;
let rxBuffer = "";

async function connect() {
  try {
    const device = await navigator.bluetooth.requestDevice({
      filters: [{ services: [0xFFE0] }]
    });

    const server = await device.gatt.connect();
    const service = await server.getPrimaryService(0xFFE0);
    bleCharacteristic = await service.getCharacteristic(0xFFE1);

    await bleCharacteristic.startNotifications();
    bleCharacteristic.addEventListener(
      "characteristicvaluechanged",
      handleData
    );

    document.getElementById("status").innerText =
      `Connected to ${device.name || "HM-10"}`;
  } catch (e) {
    document.getElementById("status").innerText = "Connection failed";
  }
}

function handleData(event) {
  const value = new TextDecoder().decode(event.target.value);
  rxBuffer += value;

  const lines = rxBuffer.split("\n");
  rxBuffer = lines.pop();

  for (const line of lines) {
    parseLine(line.trim());
  }
}

function parseLine(line) {
  if (line.startsWith("D_GPS_SPEED")) {
    document.getElementById("gps").innerText = line.split(":")[1];
  }

  if (line.startsWith("D_CALC_SPEED")) {
    document.getElementById("calc").innerText = line.split(":")[1];
  }
}

async function send(cmd) {
  if (!bleCharacteristic) {
    alert("Not connected!");
    return;
  }
  await bleCharacteristic.writeValue(
    new TextEncoder().encode(cmd + "\n")
  );
}
