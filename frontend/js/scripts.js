document.addEventListener("DOMContentLoaded", function () {
  console.log("scripts.js loaded successfully 🚀");
  loadDevices();
});

const API_BASE = "http://127.0.0.1:8000";

async function loadDevices() {
  const table = document.getElementById("activityTable");
  if (!table) return;

  table.innerHTML = "";

  try {
    const res = await fetch(API_BASE + "/devices");
    const data = await res.json();

    if (!data.devices || data.devices.length === 0) {
      table.innerHTML = `
        <tr>
          <td colspan="6">No devices connected</td>
        </tr>`;
      return;
    }

    data.devices.forEach(device => {
      const statusClass =
        device.status === "device" ? "success" : "pending";

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${device.model || "Unknown"}</td>
        <td>Android ${device.android_version || "-"}</td>
        <td>${device.serial}</td>
        <td>${device.app_version || "not installed"}</td>
        <td>
          <span class="status ${statusClass}">
            ${device.status === "device" ? "Active" : device.status}
          </span>
        </td>
        <td>
          <button class="btn" onclick="installApk('${device.serial}')">
            Install Configured APK
          </button>
        </td>
      `;
      table.appendChild(row);
    });

  } catch (err) {
    console.error(err);
    table.innerHTML = `
      <tr>
        <td colspan="6">Failed to load devices. Check the services first</td>
      </tr>`;
  }
}

function installApk(serial) {
  alert("Install APK to device: " + serial);
}
//bypass login
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // stop form submit
    window.location.href = "dashboard/index.html";
  });