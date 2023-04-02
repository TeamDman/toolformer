const done = arguments[arguments.length - 1];
const callbacks = [
  (result) => {
    console.log("Returning", result);
    done(result);
  },
];
const thing = arguments[0]; // label for what the user is picking
let timeRemaining = 25;
handle = setInterval(() => {
  timeRemaining--;
  if (timeRemaining <= 0) {
    for (const callback of callbacks) {
      callback(null);
    }
    clearInterval(handle);
  }
}, 1000);
// 1. The user clicks on the element they want to pick
// 2. A selector is generated for that element
// 3. The selector is displayed in a text input
// 4. The elements matching the selector are highlighted
// 5. The user confirms the selection and the result is returned back to python

console.log("Injecting style");
const style = document.createElement("style");
style.innerHTML = `
  #picker-message {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9998;
    background: rgba(0,0.5,0,0.5);
    color: white;
    font-size: 50px;
    font-family: Impact, Charcoal, sans-serif;
    text-stroke: 3px black;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .picker-highlight *, .picker-highlight { 
    border: 2px solid red !important;
  }

  #picker-confirm {
    position: fixed;
    top: 25px;
    left: 25px;
    width: 400px;
    height: 400px;
    cursor: move;
    display: inline-block;
  }
  #picker-confirm label, #picker-time {
    color: white;
    font-size: 20px;
    font-family: Impact, Charcoal, sans-serif;
    text-stroke: 3px black;
  }

  #picker-confirm textarea {
    display: block;
    width: 400px;
    height: 400px;
  }

  #picker-error {
    color: red;
    background-color: white;
  }
`;
document.head.appendChild(style);
callbacks.unshift(() => {
  setTimeout(() => {
    console.log("Cleaning up style", style);
    document.head.removeChild(style);
  }, 5000);
});

async function pickElement() {
  console.log("Creating message");
  const message = document.createElement("div");
  message.id = "picker-message";
  message.innerText = `CLICK THE ELEMENT.\n${thing}`;
  document.body.appendChild(message);

  return new Promise((resolve) => {
    message.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();

      // get mouse click position
      let x = e.clientX;
      let y = e.clientY;
      // remove the message (since the elements are behind it)
      document.body.removeChild(message);
      // find the element at the position
      let element = document.elementFromPoint(x, y);
      console.log("Clicked", x, y, element);
      while (element.childElementCount === 1) {
        element = element.firstElementChild;
      }
      console.log("Found", element);
      // return the element
      resolve(element);
    });
  });
}

async function getXPath(element) {
  xpath = "";
  let elements = [];
  while (element) {
    elements.unshift(element);
    let selector = "";

    const tagName = element.tagName.toLowerCase();
    selector += tagName;

    const id = element.id;
    if (id) selector += `#${id}`;

    const classes = Array.from(element.classList)
      .filter((x) => !(x.startsWith("css-") || x.startsWith("r-")))
      .join(".");
    if (classes) selector += `.${classes}`;

    const attributes = Array.from(element.attributes)
      .filter((x) => !(x.name === "class"))
      .map((x) => `[@${x.name}="${x.value}"]`)
      .join("");
    if (attributes) selector += attributes;

    if (
      true
      // tagName === "input" ||
      // tagName === "textarea" ||
      // tagName === "label" ||
      // tagName === "button" ||
      // tagName === "select"
    ) {
      let inner = element.innerText.trim();
      if (inner.length < 100 && inner.length > 0) {
        let lhs = ".";
        let rhs = inner;
        if (rhs.includes("\n")) {
          lhs = `translate(${lhs}, '&#10;', ' ')`;
          rhs = rhs.replaceAll("\n", " ");
        }
        if (rhs.includes("'")) {
          lhs = `translate(${lhs}, "'", '')`;
          rhs = rhs.replaceAll("'", "");
        }
        selector += `[contains(${lhs}, '${rhs}')]`;
      }
    }


    if (element.parentElement)
      selector += `:nth-child(${
        Array.from(element.parentElement.children).indexOf(element) + 1
      })`;

    xpath = `/${selector}${xpath}`;
    element = element.parentElement;
  }
  console.log(elements);
  console.log("XPath", xpath);
  return xpath;
}

function highlight(xpath, error) {
  try {
    //todo: use shaders and CSS clipping to replace the background of the element with animated galaxy
    const matches = document.evaluate(
      xpath,
      document,
      null,
      XPathResult.ANY_TYPE,
      null
    );
    const elements = [];
    while ((element = matches.iterateNext())) {
      elements.push(element);
    }
    console.log("Highlighting", elements);
    for (const element of elements) {
      element.classList.add("picker-highlight");
      setTimeout(() => {
        element.classList.remove("picker-highlight");
      }, 5000);
    }
  } catch (e) {
    error(e);
  }
}

async function confirmXPath(xpath) {
  const div = document.createElement("div");
  div.id = "picker-confirm";
  document.body.appendChild(div);
  div.setAttribute("draggable", "true");
  div.innerHTML = `
    <form>
      <span id="picker-time"></span>
      <label for="xpath">XPath:</label>
      <textarea id="xpath" cdkTextareaAutosize cdkAutosizeMinRows="5">${xpath}</textarea>
      <button id="picker-check" type="button">Check</button>
      <button type="submit">Confirm</button>
      <button id="picker-cancel" type="button">Cancel</button>
      <div id="picker-error"></div>
    </form>
  `;
  callbacks.unshift(() => {
    try {
      console.log("Cleaning up confirm dialog", style);
      document.body.removeChild(div);
    } catch (e) {}
  });

  setInterval(() => {
    div.querySelector("#picker-time").innerText = `${timeRemaining}s | `;
  }, 1000);
  div.querySelector("#picker-check").addEventListener("click", (e) => {
    highlight(div.querySelector("#xpath").value, (e) => {
      div.querySelector("#picker-error").innerText = e;
      setTimeout(() => {
        div.querySelector("#picker-error").innerText = "";
      }, 5000);
    });
  });
  div.querySelector("#picker-cancel").addEventListener("click", (e) => {
    document.body.removeChild(div);
    for (const callback of callbacks) {
      callback(null);
    }
  });
  highlight(div.querySelector("#xpath").value, (e) => {
    div.querySelector("#picker-error").innerText = e;
    setTimeout(() => {
      div.querySelector("#picker-error").innerText = "";
    }, 5000);
  });

  let active = true;
  div.addEventListener("dragstart", (event) => {
    // Store the initial mouse position and the element's position
    event.dataTransfer.setData(
      "text/plain",
      JSON.stringify({
        mouseX: event.clientX,
        mouseY: event.clientY,
        offsetX: event.target.offsetLeft,
        offsetY: event.target.offsetTop,
      })
    );
  });

  document.addEventListener("dragover", (event) => {
    if (!active) return;
    // Prevent the default behavior to allow dropping the element
    event.preventDefault();
  });

  document.addEventListener("drop", (event) => {
    if (!active) return;
    // Get the stored initial positions
    const data = JSON.parse(event.dataTransfer.getData("text"));

    // Calculate the new position of the draggable element
    const newLeft = event.clientX - data.mouseX + data.offsetX;
    const newTop = event.clientY - data.mouseY + data.offsetY;

    // Update the position of the draggable element
    div.style.position = "absolute";
    div.style.left = `${newLeft}px`;
    div.style.top = `${newTop}px`;

    // Prevent the default behavior
    event.preventDefault();
  });

  return new Promise((resolve) => {
    div.querySelector("form").addEventListener("submit", (e) => {
      active = false;
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      const xpath = div.querySelector("#xpath").value;
      document.body.removeChild(div);
      resolve(xpath);
    });
  });
}

async function main() {
  const result = await pickElement();
  let xpath = await getXPath(result);
  xpath = await confirmXPath(xpath);
  for (const callback of callbacks) {
    callback(xpath);
  }
}
main();

// function preprocess(list, keyGetter, priority, disallowPred) {
//   return Array.from(list)
//     .filter((x) => !disallowPred(keyGetter(x)))
//     .sort((a, b) => {
//       a = keyGetter(a);
//       b = keyGetter(b);
//       const aInPriority = priority.includes(a);
//       const bInPriority = priority.includes(b);

//       if (aInPriority && bInPriority) {
//         return 0;
//       } else if (aInPriority) {
//         return -1;
//       } else if (bInPriority) {
//         return 1;
//       } else {
//         return a.localeCompare(b);
//       }
//     });
// }

// function getDirectInnerText(element) {
//   return Array.from(element.childNodes)
//     .filter((node) => node.nodeType === Node.TEXT_NODE)
//     .map((node) => node.textContent)
//     .join("");
// }

// function getXPath(element) {
//   function getUniqueXPath(el) {
//     let tagName = el.tagName.toLowerCase();

//     let xpath = `./${tagName}`;

//     function isUnique() {
//       const found = document.evaluate(
//         `count(${xpath})`,
//         el.parentElement,
//         null,
//         XPathResult.NUMBER_TYPE,
//         null
//       ).numberValue;
//       if (found < 1) {
//         console.log(el.parentElement, xpath);
//         throw new Error("XPath found no elements");
//       }
//       return found === 1;
//     }

//     if (el.id) {
//       xpath += `[@id='${el.id}']`;
//       // if (isUnique()) return xpath;
//     }

//     if (
//       tagName === "input" ||
//       tagName === "textarea" ||
//       tagName === "label" ||
//       tagName === "button" ||
//       tagName === "select"
//     ) {
//       // const inner = getDirectInnerText(el).trim();
//       let inner = el.innerText.trim();
//       if (inner.length < 100 && inner.length > 0) {
//         let lhs = ".";
//         let rhs = inner;
//         if (rhs.includes("\n")) {
//           lhs = `translate(${lhs}, '&#10;', ' ')`;
//           rhs = rhs.replaceAll("\n", " ");
//         }
//         if (rhs.includes("'")) {
//           lhs = `translate(${lhs}, "'", '')`;
//           rhs = rhs.replaceAll("'", "");
//         }
//         xpath += `[contains(${lhs}, '${rhs}')]`;

//         // if (isUnique()) return xpath;
//       }
//     }

//     for (const a of preprocess(
//       el.attributes,
//       (x) => x.name,
//       ["autocomplete", "href"],
//       (x) => false
//     )) {
//       if (a.name === "id" || a.name === "class" || a.name === "style") continue;
//       xpath += `[@${a.name}='${a.value}']`;
//       // if (isUnique()) return xpath;
//     }

//     if (el.classList.length > 0) {
//       for (const className of preprocess(
//         el.classList,
//         (x) => x,
//         [],
//         (x) => x.startsWith("css-") || x.startsWith("r-")
//       )) {
//         xpath += `[contains(concat(' ', normalize-space(@class), ' '), ' ${className} ')]`;
//         // if (isUnique()) return xpath;
//       }
//     }

//     // const index = Array.from(el.parentNode.children)
//     //   .filter((sibling) => sibling.tagName.toLowerCase() === tagName)
//     //   .indexOf(el);
//     // xpath = `./${tagName}[${index + 1}]`;

//     return xpath;
//   }

//   // get the innermost element
//   while (element.childNodes.length === 1 && element.firstChild.nodeType === 1) {
//     element = element.firstChild;
//   }
//   const elements = [];
//   let current = element;
//   while (current.parentElement) {
//     elements.unshift(current);
//     current = current.parentElement;
//   }
//   console.log(
//     "elements",
//     elements.map((x) => [x, x.textContent, x.innerText])
//   );
//   return "/" + elements.map(getUniqueXPath).join("/");
// }
// function getSelector(el) {
//   const selector = getXPath(el);
//   return selector;
//   //   const elements = [];
//   //   let current = el;

//   //   while (current.parentElement) {
//   //     elements.unshift(current);
//   //     current = current.parentElement;
//   //   }

//   //   return elements.map(getXPath).join(" > ");
// }

// window.get = xpath => {
//   return document.evaluate(
//     xpath,
//     document,
//     null,
//     XPathResult.FIRST_ORDERED_NODE_TYPE,
//     null
//   ).singleNodeValue
// }

// /*
// */

// // function getUniqueSelector(element) {
// //   while (element.childNodes.length === 1 && element.firstChild.nodeType === 1)
// //     element = element.firstChild;
// //   let selector = element.tagName.toLowerCase();
// //   function isUnique() {
// //     return (
// //       [...element.parentElement.children].filter((sibling) =>
// //         sibling.matches(selector)
// //       ).length === 1
// //     );
// //   }

// //   if (element.id) {
// //     selector += `#${element.id}`;
// //     if (isUnique()) return selector;
// //   }
// //   for (const a of preprocess(
// //     element.attributes,
// //     (x) => x.name,
// //     ["autocomplete", "href"],
// //     (x) => false
// //   )) {
// //     if (a.name === "id" || a.name === "class" || a.name === "style") continue;
// //     selector += `[${a.name}="${a.value}"]`;
// //     if (isUnique()) return selector;
// //   }

// //   if (element.classList.length > 0) {
// //     for (const className of preprocess(
// //       element.classList,
// //       (x) => x,
// //       ["content"],
// //       (x) => x.startsWith("css-") || x.startsWith("r-")
// //     )) {
// //       selector += `.${className}`;
// //       if (isUnique()) return selector;
// //     }
// //   }

// //   const siblingSameType = [...element.parentElement.children].filter(
// //     (sibling) => sibling.tagName.toLowerCase() === selector
// //   );
// //   if (siblingSameType.length === 1) return selector;
// //   const index = siblingSameType.indexOf(element);
// //   selector += `:nth-of-type(${index + 1})`;

// //   return selector;
// // }
