const randomUnique = (range, count) => {
  // Will give from [1, N) range
  console.assert(range >= count, "Invalid values for range and count");
  if (range >= count) {
    let nums = new Set();
    while (nums.size < count) {
      nums.add(Math.floor(Math.random() * (range - 1) + 1));
    }
    return [...nums];
  } else {
    return [];
  }
};

function getRandomArbitrary(min, max) {
  // Min included max not included
  return Math.floor(Math.random() * (max - min) + min);
}

function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const random_min_max = (min, max, count) => {
  // Min included max not included
  console.assert(max - min >= count, "Invalid values for range and count");
  if (max - min >= count) {
    let nums = new Set();
    while (nums.size < count) {
      nums.add(getRandomArbitrary(min + 1, max));
    }
    return [...nums];
  } else {
    return [];
  }
};

function getNRandomFromArray(arr, n) {
  var result = new Array(n),
    len = arr.length,
    taken = new Array(len);
  if (n > len)
    throw new RangeError("getRandom: more elements taken than available");
  while (n--) {
    var x = Math.floor(Math.random() * len);
    result[n] = arr[x in taken ? taken[x] : x];
    taken[x] = --len in taken ? taken[len] : len;
  }
  return result;
}
