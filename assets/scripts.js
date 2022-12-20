function printData()

{

    var divToPrint=document.getElementById("ImagenPadre");

    newWin= window.open("");

    newWin.document.write(divToPrint.outerHTML);

    newWin.print();

    newWin.close();

}

setTimeout(function mainFunction(){

    try {

		// Ini

		
        document.getElementById("btn-Descargar").addEventListener("click", function(){

			alert("Hola");
            printData();

        })

		// Fin
	}

	catch(err) {

	  console.log(err)

	}

  console.log('Listener Added!');

}, 5000);