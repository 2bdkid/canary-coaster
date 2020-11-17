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
	
	<script src="cbor-js/cbor.js" type="text/javascript"></script>
	<script>
		webSocket = new WebSocket("ws://50.90.141.26:5688");
		webSocket.binaryType = "arraybuffer";
		webSocket.onmessage = function (event) {
			weights = CBOR.decode(event.data);
			
			document.getElementById("data").innerHTML = "";
			document.getElementById("tareButton").innerHTML = "";
			for(const [key, value] of Object.entries(weights))
			{
				document.getElementById("data").innerHTML += key + ": " + parseFloat(value).toFixed(2);
				document.getElementById("tareButton").innerHTML += '<button onclick="webSocket.send(`'+key+'`); console.log(`'+key+'`)">Tare '+key+'</button>';
			}
		}
	</script>
		<!-- Header -->
			<header id="header" class="alt">
				<nav id="nav">
					<ul>
						<li><a href="index.php">Home</a></li>
						<li><a href="index.php">Generic</a></li>
						<li><a href="index.php">Elements</a></li>
					</ul>
				</nav>
			</header>

			<a href="#menu" class="navPanelToggle"><span class="fa fa-bars"></span></a>

		<!-- Banner -->
			<section id="banner">
				<h2>Canary Coaster Dashboard</h2>
				<p>Completed by Brady Dean and Jake Waggoner</p>
			</section>

			<section id="one" class="wrapper style1">
				<div class="container">
					<header class="major">
						<h2 id="data" name="data">Data</h2>
						<div id="tareButton" name = "tareButton"></div>
					</header>
				</div>
			</section>
			
		<!-- Divider -->
		<section id="four" class="wrapper style3 special"></section>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>