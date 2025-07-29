fetch("http://backend/data")
  .then(res => res.json())
  .then(data => {
    document.getElementById("data").innerText = JSON.stringify(data);
  });

