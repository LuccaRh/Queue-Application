const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = function() {
  document.getElementById("wsStatus").textContent = "✓ Connected";
};

socket.onclose = function() {
  document.getElementById("wsStatus").textContent = "✗ Disconnected";
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
      <small>Status: ${client.status} | Tried: ${tried}</small>
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
      <strong>#${index + 1} - ${operator.name || operator.id}</strong><br/>
      <small>Status: ${operator.status || ""} | Ringing ID: ${operator.ringing_call_id || "none"}</small>
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
      <small>${call.operator.name || call.operator.id} → ${call.client.name || call.client.id}</small>
    `;
    ul.appendChild(li);
  });
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
      <small>${call.operator.name || call.operator.id} ↔ ${call.client.name || call.client.id}</small>
    `;
    ul.appendChild(li);
  });
}


document.getElementById("clientform").addEventListener("submit", async function(event) {
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

document.getElementById("operatorform").addEventListener("submit", async function(event) {
  event.preventDefault();

  const name = document.getElementById("operatorName").value;

  const response = await fetch("http://localhost:8000/operators", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: name
    })
  });

  const data = await response.json();
  console.log(data);
  alert(data.message);
});