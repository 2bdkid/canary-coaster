<!DOCTYPE HTML>
<html>
	<link rel="shortcut icon" type="image/ico" href="images/canary.jpg">
	<head>
		<title>Canary Coaster Dashboard</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="assets/css/main.css" />
	</head>
	<body class="landing">
	
	<script src="cbor.js" type="text/javascript"></script>
	<script>
		webSocket = new WebSocket("ws://50.90.141.26:5688");
		webSocket.binaryType = "arraybuffer";
		webSocket.onmessage = function (event) {
			weights = CBOR.decode(event.data);
			var pathToImage = "images/";
			for(const [key, value] of Object.entries(weights))
			{
				if(document.body.contains(document.getElementById(key)) == false)
				{
					var container = document.getElementById("head");
				
					var wrapper = document.createElement("DIV");
					wrapper.className = "2u"; //For grid-like layout
					wrapper.id = key;

					var spacer = document.createElement("DIV");
					spacer.className = "1u";

					var image = document.createElement("IMG");
					image.src = pathToImage+"X.png";
					image.id = key+"_img";
					image.style.height = "180px";
					image.style.width = "123px";

					var form = document.createElement("FORM");
					form.setAttribute("method", "post");
						var label = document.createElement("STRONG");
						label.innerText = "Drink Type";
						form.appendChild(label);

						var input = document.createElement("INPUT");
						input.type = "text";
						input.placeholder = "Enter the drink here"
						input.id = key+"_input";
						input.value = sessionStorage.getItem(key);
						form.appendChild(input);
						input.addEventListener("click", function(){input.classList.toggle("active");});

						var saveButton = document.createElement("BUTTON");
						saveButton.innerHTML = "Save drink type";
						saveButton.addEventListener("click",function(){sessionStorage.setItem(key, input.value); input.value = sessionStorage.getItem(key);})
						form.appendChild(saveButton);

					var button = document.createElement("BUTTON");
					button.innerHTML = "Tare "+key;
					button.addEventListener("click",function(){webSocket.send(key);});

					wrapper.appendChild(image);
					wrapper.appendChild(form);
					wrapper.appendChild(button);
					container.appendChild(spacer);
					container.appendChild(wrapper);
				}

				var weight = parseFloat(value).toFixed(2);
				var image = document.getElementById(key+"_img");
				weight = 700;
				if(weight > 670)
				{
					image.src = pathToImage+"FullGlass.PNG";
					image.title = "Glass is full!";
				}
				else if(weight > 600 && weight <= 670)
				{
					image.src = pathToImage+"MostlyFullGlass.PNG";
					image.title = "Glass is mostly full!";
				}
				else if(weight > 530 && weight <= 600)
				{
					image.src = pathToImage+"HalfWayFullGlass.PNG";
					image.title = "Glass is halfway full!";
				}
				else if(weight > 430 && weight <= 530)
				{
					image.src = pathToImage+"MostlyEmptyGlass.PNG";
					image.title = "Glass is mostly empty!";
				}
				else if(weight > 320 && weight <= 430)
				{
					image.src = pathToImage+"ExlamGlass.png";
					image.title = "Glass is empty and needs to be refilled!";
				}
				else
				{
					image.src = pathToImage+"X.png";
					image.title = "Drink is not on the coaster";
				}
			}
		}
	</script>

		<!-- Banner -->
			<section id="banner">
				<h2>Canary Coaster Dashboard</h2>
				<p>Completed by Brady Dean and Jake Waggoner</p>
			</section>

			<section id="one" class="wrapper style1">
				<div class="box alt">
					<div class="row uniform 25%" id="head">
					</div>
				</div>
			</section>
			
		<!-- Footer -->
		<footer id="footer">
			<div class="container">
				<ul class="icons">
					<li><a href="https://github.iu.edu/bddean/iot-project3">GitHub</a></li>
				</ul>
				<ul class="copyright">
					<li>Created By Brady Dean and Jake Waggoner</li>
				</ul>
			</div>
		</footer>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>