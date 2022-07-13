document.addEventListener("DOMContentLoaded", function() {

  document.querySelectorAll(".unarchive--box").forEach(element2 => {
        element2.addEventListener("click", function (ee) {
            $(document).one('submit', element2, function (fff) {
                fff.preventDefault()
                $.ajax({
                    type:'POST',
                    url:'/create/',
                    data:{
                      id:$(element2).val(),
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                    },
                    success: function () {

                    },
                });
            });
            let rodzicc = element2.parentElement.parentElement;
            if (rodzicc.style.color === "" || rodzicc.style.color === "black") {
              rodzicc.style.color = "#7F8177"
            } else {
              rodzicc.style.color = "black"
            }

            if (element2.style.backgroundColor === "red" || element2.style.backgroundColor === "") {
              element2.style.backgroundColor = "green";
            } else {
              element2.style.backgroundColor = "red"
            }


        });
    });

  document.querySelectorAll(".archive--box").forEach(element => {
        element.addEventListener("click", function (e) {
            $(document).one('submit', element, function (ff) {
                ff.preventDefault()
                $.ajax({
                    type:'POST',
                    url:'/create/',
                    data:{
                      id:$(element).val(),
                      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),

                    },
                    success: function () {

                    },
                });
            });
            let rodzic = element.parentElement.parentElement;
            if (rodzic.style.color === "" || rodzic.style.color === "black") {
              rodzic.style.color = "#7F8177"
            } else {
              rodzic.style.color = "black"
            }

            if (element.style.backgroundColor === "green" || element.style.backgroundColor === "") {
              element.style.backgroundColor = "red";
            } else {
              element.style.backgroundColor = "green"
            }


        });
    });

  class Settings {
    constructor($eee, $sett) {
      this.$eee = $eee;
      this.$settingsButton = $eee.querySelector(".right--profile input[name='send_button']");
      this.$passwordButton = $eee.querySelector(".pw--change--box input[name='niccc']");
      this.$settBTN = $sett.querySelector(".guzikUstawien");
      this.init();


    }

    init() {
      // this.changeSettings();
      // this.changePassword();
      this.events();
    }

    events() {
      if (window.location.href === "http://127.0.0.1:8000/settings") {
        this.changeSettings()
      }
      if (window.location.href === "http://127.0.0.1:8000/settings/change-password") {
        this.changePassword()

      // this.$settBTN.addEventListener("click", changeSettings)

      }}

    changeSettings() {
      function settingsButtonFunction(event) {
        let pw = document.querySelector(".right--profile input[name='pass']");
        let pw_given = prompt("Enter your password");
        if (pw_given) {
          pw.value = pw_given;
        }
      }

      this.$settingsButton.addEventListener("click", settingsButtonFunction);

    };

    changePassword(e) {
      function passwordButtonFunction(event) {
        let errorMsg = document.querySelector(".error--password");
        if (errorMsg.childNodes.length !== 0) {
          alert("xxx");
        }
      }
      this.$passwordButton.addEventListener("click", passwordButtonFunction);

    };
  }
  const glowne = document.querySelector(".header--form-page");
  const settingsDropdown = document.querySelector(".dropdown")
  if (glowne !== null) {
    new Settings(glowne, settingsDropdown);
  }










  // document.querySelectorAll(".table--donations button").forEach(element => {
  //   element.addEventListener("click", function () {
  //     this.parentElement.parentElement.style.backgroundColor = "#f1f1f1"
  //   })
  // })






  /**
   * HomePage - Help section
   */




  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */

    step_1_categories() {
      let inputs = document.querySelector("form").firstElementChild.querySelectorAll("input[name=categories]")

      let categories = []
      inputs.forEach(input => {
        if (input.checked === true) {
          categories.push(input.value)
        }
      })
      return categories
    }


    step_2_data() {

      // let address = document.querySelector("form").elements.address.value

      let form_2_data = {
        "address":document.querySelector("input[name=address]").value,
        "city":document.querySelector("input[name=city]").value,
        "postalCode":document.querySelector("input[name=postcode]").value,
        "telNumb":document.querySelector("input[name=phone]").value,
        "date":document.querySelector("input[name=data]").value,
        "time":document.querySelector("input[name=time]").value,
        "comments": document.querySelector("textarea[name=more_info]").value,
      }
      return form_2_data
    }


    updateForm() {

      this.$step.innerText = this.currentStep;


      if (this.$step.innerText === "3") {

        // console.log(this.step_1_categories(), ' These are the chosen categories...')
        const chosenCategories = this.step_1_categories()
        document.querySelectorAll('.institution').forEach(function (div) {
          // console.log(div, div.dataset.categories)
          const myArray = div.dataset.categories.split(" ")
          const isIncluded = chosenCategories.some( item => myArray.includes(item))
          if (isIncluded === false) {
            div.style.display = "none";
          } else {
            div.style.display = "block";
          }
        })
      }

      if (this.$step.innerText === "4") {

          let categoriesNames = []
        let checkedCategories = document.querySelector("form").firstElementChild.querySelectorAll("input[name=categories]")
        checkedCategories.forEach(item => {
          if (item.checked === true) {
            categoriesNames.push(item.nextElementSibling.nextElementSibling.innerText)

          }
        })
        console.log(categoriesNames)

        let summaryButton = document.querySelector(".summary-button")
        summaryButton.addEventListener("click", evt => {
          let step_3_divs = document.querySelectorAll(".institution")
          let institution = ""
          step_3_divs.forEach(div => {
            if (div.querySelector("input").checked) {
              institution = div.querySelector(".title").innerText
            }
          })
          document.querySelector(".checked_org").value = institution
          let numberOfBags = document.querySelector("div [data-step='2'] input").value
          let categoriesNamesSpace = categoriesNames.join(', ');
          if (numberOfBags <= 1) {
            numberOfBags = numberOfBags + " bag with: " + categoriesNames
          } else {
            numberOfBags = numberOfBags + " bags with: " + categoriesNamesSpace
          }

          let recipient = "For: " + institution

          console.log(numberOfBags)
          let summary = document.querySelector(".summary");
          summary.querySelector(".icon-bag").nextElementSibling.innerText = numberOfBags;
          summary.querySelector(".icon-hand").nextElementSibling.innerText = recipient;

          summary.lastElementChild.firstElementChild.querySelector("ul").innerHTML = `
            <li>${this.step_2_data().address}</li>
            <li>${this.step_2_data().city}</li>
            <li>${this.step_2_data().postalCode}</li>
            <li>${this.step_2_data().telNumb}</li>`
            summary.lastElementChild.lastElementChild.querySelector("ul").innerHTML = `
            <li>${this.step_2_data().date}</li>
            <li>${this.step_2_data().time}</li>
            <li>${this.step_2_data().comments}</li>`
        })
      }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
        this.$step.parentElement.hidden = this.currentStep >= 6;
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      // e.preventDefault();
      this.currentStep++;
      this.updateForm();
      document.querySelector(".categories_all").value = this.step_1_categories()

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
