
async function loadEvents() {
  const res = await fetch("/events");
  const data = await res.json();

  const list = document.getElementById("events");
  list.innerHTML = "";

  data.forEach(e => {
    let text = "";
    const time = new Date(e.timestamp).toUTCString();

    if (e.action === "PUSH") {
      text = `${e.author} pushed to ${e.to_branch} on ${time}`;
    } 
    else if (e.action === "PULL_REQUEST") {
      text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${time}`;
    } 
    else if (e.action === "MERGE") {
      text = `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${time}`;
    }

    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });
}

loadEvents();
setInterval(loadEvents, 15000);
