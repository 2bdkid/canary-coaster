<!DOCTYPE HTML>
<!--
	Author: Jake Waggoner
	Template Used: Spatial
	Date: 9-5-2020
	Filename: lab1.php
-->
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
			
			document.getElementById("data").innerHTML = "";
			document.getElementById("tareButton").innerHTML = "";
			for(const [key, value] of Object.entries(weights))
			{
				var weight = parseFloat(value).toFixed(2);
				var image = document.getElementById("cup");
				var pathToImage = "images/";
				if(weight > 670)
				{
					image.src = pathToImage+"FullGlass.PNG";
					image.style.height = "180px";
					image.style.width = "123px";
				}
				else if(weight > 600 && weight <= 670)
				{
					image.src = pathToImage+"MostlyFullGlass.PNG";
					image.style.height = "180px";
					image.style.width = "123px";
				}
				else if(weight > 530 && weight <= 600)
				{
					image.src = pathToImage+"HalfWayFullGlass.PNG";
					image.style.height = "180px";
					image.style.width = "123px";
				}
				else if(weight > 430 && weight <= 530)
				{
					image.src = pathToImage+"MostlyEmptyGlass.PNG";
					image.style.height = "180px";
					image.style.width = "123px";
				}
				else if(weight > 320 && weight <= 430)
				{
					image.src = pathToImage+"EmptyGlass.PNG";
					image.style.height = "180px";
					image.style.width = "123px";
				}
				else
				{
					image.src = pathToImage+"X.png";
					image.style.height = "110px";
					image.style.width = "110px";
				}
				document.getElementById("data").innerHTML += key + ": " + parseFloat(value).toFixed(2);
				document.getElementById("tareButton").innerHTML += '<button onclick="webSocket.send(`'+key+'`)">Tare '+key+'</button>';
			}
		}
	</script>

		<!-- Banner -->
			<section id="banner">
				<h2>Canary Coaster Dashboard</h2>
				<p>Completed by Brady Dean and Jake Waggoner</p>
			</section>

			<section id="one" class="wrapper style1">
				<div class="container">
					<header class="major">
						<img id="cup" src="images/FullGlass.PNG"><br>
						<p id="data" name="data">Data</p>
						<div id="tareButton" name = "tareButton"></div>
					</header>
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