// Load employee data and display as cards
fetch('data/employees.json')
  .then(response => response.json())
  .then(employees => {
    const container = document.getElementById('employee-container');

    employees.forEach(emp => {
      const card = document.createElement('div');
      card.className = 'card';

      card.innerHTML = `
        <h3>${emp.name}</h3>
        <p>Status: ${emp.status}</p>
        <p>Last Input: ${emp.last_input}</p>
        <p>Call State: ${emp.call_state}</p>
        <p>Auto Clock-Outs: ${emp.auto_clock_outs}</p>
        <p>Manager: ${emp.manager}</p>
        <p>${emp.alert ? '⚠️ Alert' : ''}</p>
      `;

      container.appendChild(card);
    });
  });
