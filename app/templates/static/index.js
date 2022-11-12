"use strict";

const logInBt = document.querySelector("#logInBt");
logInBt.addEventListener("click", async function (e) {
  e.preventDefault();
  const nameArea = document.querySelector("#nameArea");
  const data = {
    user_name: nameArea.value,
  };
  const req = await fetch("/user_logIn", {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const res = await req.json();
  console.log(res.customer_id);
});
