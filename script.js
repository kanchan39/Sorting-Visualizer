function startSorting() {
    let algorithm = document.getElementById("algorithm").value;
    let array = [...Array(20)].map(() => Math.floor(Math.random() * 100) + 1);

    fetch('/sort', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ algorithm, array })
    })
    .then(response => response.json())
    .then(data => visualizeSorting(data.steps));  // Use "data.steps" as JSON returns an object
}

function visualizeSorting(steps) {
    let bars = document.getElementById("bars");
    
    // Generate initial bars
    bars.innerHTML = steps[0][0].map(val => 
        `<div class="bar" style="height: ${val * 3}px;"></div>`
    ).join('');

    let index = 0;

    function animate() {
        if (index < steps.length) {
            let [arr, highlights] = steps[index];
            let barElements = document.getElementsByClassName("bar");

            for (let i = 0; i < arr.length; i++) {
                barElements[i].style.height = `${arr[i] * 3}px`;
                barElements[i].classList.remove("highlight", "sorted");
            }

            highlights.forEach(i => barElements[i].classList.add("highlight"));

            index++;
            setTimeout(animate, 200);
        } else {
            document.querySelectorAll(".bar").forEach(bar => bar.classList.add("sorted"));
        }
    }

    animate();
}
