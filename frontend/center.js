document.addEventListener("DOMContentLoaded", () => {
  const socket = new WebSocket("ws://localhost:8000/ws");

  socket.onopen = function() {
    const status = document.getElementById("wsStatus");
    if (status) status.textContent = "✓ Connected";
  };

  socket.onclose = function() {
    const status = document.getElementById("wsStatus");
    if (status) status.textContent = "✗ Disconnected";
  };

  socket.onmessage = function(event) {
    try {
      const msg = JSON.parse(event.data);
      if (msg.data && msg.data.clients_queue) {
        updateClientList(msg.data.clients_queue);
      }
      if (msg.data && msg.data.operators_queue) {
        updateOperatorList(msg.data.operators_queue);
      }
      if (msg.data && msg.data.ringing_calls) {
        updateRingingList(msg.data.ringing_calls);
      }
      if (msg.data && msg.data.accepted_calls) {
        updateAcceptedList(msg.data.accepted_calls);
      }
    } catch (err) {
      console.error("Parse error:", err);
    }
  };

  const clientForm = document.getElementById("clientform");
  if (clientForm) {
    clientForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      const name = document.getElementById("clientName").value;
      try {
        await fetch("http://localhost:8000/clients", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name })
        });
        document.getElementById("clientName").value = "";
      } catch (err) {
        console.error("Error creating client:", err);
      }
    });
  }

  const operatorForm = document.getElementById("operatorform");
  if (operatorForm) {
    operatorForm.addEventListener("submit", async function(event) {
      event.preventDefault();
      const name = document.getElementById("operatorName").value;
      try {
        const response = await fetch("http://localhost:8000/operators", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name })
        });
        const data = await response.json();
        console.log(data);
        if (data.message) alert(data.message);
        document.getElementById("operatorName").value = "";
      } catch (err) {
        console.error("Error creating operator:", err);
      }
    });
  }
});

function updateClientList(clients) {
  const ul = document.getElementById("clients");
  ul.innerHTML = "";
  
  if (clients.length === 0) {
    ul.innerHTML = "<li><em>No clients waiting</em></li>";
    return;
  }
  
  clients.forEach((client, index) => {
    const li = document.createElement("li");
    const tried = client.tried_operators && client.tried_operators.length > 0 
      ? client.tried_operators.join(", ") 
      : "none";
    
    li.innerHTML = `
      <strong>#${index + 1} - ${client.name || client.id}</strong><br/>
      <small>Id: ${client.id} | Status: ${client.status} | Tried: ${tried}</small>
    `;
    ul.appendChild(li);
  });
}

function updateOperatorList(operators) {
  const ul = document.getElementById("operators");
  ul.innerHTML = "";

  if (operators.length === 0) {
    ul.innerHTML = "<li><em>No operators waiting</em></li>";
    return;
  }

  operators.forEach((operator, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>#${index + 1} - ${operator.name}</strong><br/>
      <small>Status: ${operator.status} | ID: ${operator.id}</small>
    `;
    ul.appendChild(li);
  });
}

function updateRingingList(calls) {
  const ul = document.getElementById("ringing");
  ul.innerHTML = "";

  if (calls.length === 0) {
    ul.innerHTML = "<li><em>No ringing calls</em></li>";
    return;
  }

  calls.forEach((call) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>Ringing ID: ${call.id}</strong><br/>
      <small>Operator: ${call.operator.name} (${call.operator.id}) → Client: ${call.client.name} (${call.client.id})</small><br/>
      <button onclick="acceptCall('${call.operator.id}')">Accept</button>
      <button onclick="rejectCall('${call.operator.id}')">Reject</button>
    `;
    ul.appendChild(li);
  });
}

async function acceptCall(operatorId) {
  try {
    await fetch("http://localhost:8000/accept", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({operator: operatorId})
    });
  } catch (err) {
    console.error("Error accepting call:", err);
  }
}

async function rejectCall(operatorId) {
  try {
    await fetch("http://localhost:8000/reject", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({operator: operatorId})
    });
  } catch (err) {
    console.error("Error rejecting call:", err);
  }
}

function updateAcceptedList(calls) {
  const ul = document.getElementById("accepted");
  ul.innerHTML = "";

  if (calls.length === 0) {
    ul.innerHTML = "<li><em>No accepted calls</em></li>";
    return;
  }

  calls.forEach((call) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>Accepted ID: ${call.id}</strong><br/>
      <small>Operator: ${call.operator.name} (${call.operator.id}) → Client: ${call.client.name} (${call.client.id})</small>
    `;
    ul.appendChild(li);
  });
}