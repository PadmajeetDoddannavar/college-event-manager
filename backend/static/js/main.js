// Load events in Student UI
async function loadEventsTable() {
  const res = await fetch("/events");
  const data = await res.json();
  const tbody = document.querySelector("#eventsTable tbody");
  tbody.innerHTML = "";
  data.forEach(e => {
    tbody.innerHTML += `
      <tr>
        <td>${e.title}</td>
        <td>${e.event_type}</td>
        <td>${e.college}</td>
        <td>${new Date(e.start_time).toLocaleString()}</td>
        <td>${new Date(e.end_time).toLocaleString()}</td>
        <td>${e.location || "-"}</td>
      </tr>`;
  });
}

// Load Event Popularity Report (Chart.js)
async function loadReports() {
  const res = await fetch("/reports/event-popularity");
  const data = await res.json();
  const labels = data.map(r => r.event);
  const counts = data.map(r => r.registrations);

  new Chart(document.getElementById("eventChart"), {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Registrations",
        data: counts,
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }]
    }
  });
}

// Load Student Participation Report (Chart.js)
async function loadParticipation() {
  const res = await fetch("/reports/student-participation");
  const data = await res.json();
  const labels = data.map(r => r.student);
  const counts = data.map(r => r.events);

  new Chart(document.getElementById("participationChart"), {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56", "#4BC0C0"]
      }]
    }
  });
}
