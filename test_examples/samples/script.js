function calculateStats(numbers) {
    if (!numbers || numbers.length === 0) {
        return null;
    }

    let sum = 0;
    let max = numbers[0];
    let min = numbers[0];

    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
        if (numbers[i] > max) max = numbers[i];
        if (numbers[i] < min) min = numbers[i];
    }

    const avg = sum / numbers.length;

    return {
        sum: sum,
        average: avg,
        max: max,
        min: min
    };
}

const data = [10, 20, 5, 100, 45];
const stats = calculateStats(data);
console.log(stats);
