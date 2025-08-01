fetch("http://aef32ee27a0b040beafc3e196d6ca001-305758529.ap-south-1.elb.amazonaws.com/data")
  .then(res => {
    if (!res.ok) throw new Error("Failed to fetch data");
    return res.json();
  })
  .then(data => {
    console.log("Fetched data:", data);
    document.getElementById("data").innerText = JSON.stringify(data, null, 2);
  })
  .catch(error => {
    console.error("Error fetching backend data:", error);
    document.getElementById("data").innerText = "Error fetching backend data";
  });
