document.addEventListener("DOMContentLoaded", function () {
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
    document.addEventListener("click", function (e) {
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
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});


const filterFunction = function () {
    /**
     * Filtering organization list by category
     */
    let step1 = document.querySelectorAll("input[type=checkbox]");
    let step2 = document.querySelectorAll("input[type=radio]");
    let button = document.querySelector(".next-step");

    if (button) {
        button.addEventListener("click", () => {
            step2.forEach(radio => {
                radio.parentElement.parentElement.hidden = true;
                step1.forEach(checkbox => {
                    if (checkbox.checked) {
                        let radioText = radio.id;
                        if (radioText.includes(checkbox.nextElementSibling.nextElementSibling.textContent.toLowerCase())) {
                            radio.parentElement.parentElement.hidden = false;
                        }
                    }
                })
            })
        })
    }
}


filterFunction();

const insertFunction = function () {
    /* Insert data from prev steps into final step fields
    */
    let nextBtn = document.querySelectorAll(".next-step");
    let prevBtn = document.querySelectorAll(".prev-step");
    let index = 0; //index count the steps in the form //
    nextBtn.forEach(next => {
            next.addEventListener("click", () => {
                index = index + 1;
                if (index === 4) {
                    //input data variables//
                    let bags = document.querySelector("input[name=bags]");
                    let category = document.querySelectorAll("input[type=checkbox]");
                    let receiver = document.querySelectorAll("input[type=radio]");
                    let adress = document.querySelector("input[name=address]");
                    let city = document.querySelector("input[name=city]");
                    let code = document.querySelector("input[name=postcode]");
                    let phoneNumber = document.querySelector("input[name=phone]");
                    let data = document.querySelector("input[name=data]");
                    let time = document.querySelector("input[name=time]");
                    let info = document.querySelector("textarea");
                    //variables to complete//
                    let summaryTextHow = document.querySelector(".icon-bag");
                    let summaryTextWho = document.querySelector(".icon-hand");
                    let summary = document.querySelector(".summary");
                    let summaryAddress = summary.querySelector(".form-section--columns");
                    let checkedCategories = '';
                    let checkedOrganization = '';

                    let donationAddress = document.createElement("ul");
                    donationAddress.innerHTML = `<li>${adress.value}</li>
                                                 <li>${city.value}</li>
                                                 <li>${code.value}</li>
                                                 <li>${phoneNumber.value}</li>`;
                    let donationInfo = document.createElement("ul");
                    donationInfo.innerHTML = `<li>${data.value}</li>
                                              <li>${time.value}</li>
                                              <li>${info.value}</li>`;
                    category.forEach(el => {
                        if (el.checked) {
                            checkedCategories = `${checkedCategories} ${el.nextElementSibling.nextElementSibling.textContent.toLowerCase()},`;
                        }
                    })
                    receiver.forEach(radio => {
                        if (radio.checked) {
                            checkedOrganization = radio.nextElementSibling.nextElementSibling.firstElementChild.textContent;
                        }
                    })
                    if (bags.value < 2) {
                        summaryTextHow.nextElementSibling.textContent = `${bags.value} worek a w nim: ${checkedCategories.slice(0, -1)}`;
                    } else if (bags.value >= 2 && bags.value <= 4) {
                        summaryTextHow.nextElementSibling.textContent = `${bags.value} worki a w nich: ${checkedCategories.slice(0, -1)}`;
                    } else if (bags.value >= 5) {
                        summaryTextHow.nextElementSibling.textContent = `${bags.value} work??w a w nich: ${checkedCategories.slice(0, -1)}`;
                    }
                    summaryTextWho.nextElementSibling.textContent = `Odbiorca: ${checkedOrganization}`;
                    summaryAddress.firstElementChild.replaceChild(donationAddress,
                        summaryAddress.firstElementChild.firstElementChild.nextElementSibling);
                    summaryAddress.lastElementChild.replaceChild(donationInfo,
                        summaryAddress.firstElementChild.nextElementSibling.firstElementChild.nextElementSibling);


                }
            })
        }
    )
    prevBtn.forEach(prev => {
            prev.addEventListener("click", () => {
                index = index - 1;
            })
        }
    )
}

insertFunction()

const sendData = () => {
    // function make json file and send it to backend
    //after save donation in db we are redirected to confirmation site
    let submitBtn = document.querySelector("button[type=submit]");
    submitBtn.addEventListener("click", () => {
        let bags = document.querySelector("input[name=bags]");
        let category = document.querySelectorAll("input[type=checkbox]");
        let receiver = document.querySelectorAll("input[type=radio]");
        let adress = document.querySelector("input[name=address]");
        let city = document.querySelector("input[name=city]");
        let code = document.querySelector("input[name=postcode]");
        let phoneNumber = document.querySelector("input[name=phone]");
        let data = document.querySelector("input[name=data]");
        let time = document.querySelector("input[name=time]");
        let info = document.querySelector("textarea");
        let checkCategories = [];
        let organization = '';

        category.forEach(el => {
            if (el.checked) {
                checkCategories.push(el.id);
            }
        })
        receiver.forEach(radio => {
            if (radio.checked) {
                organization = radio.nextElementSibling.nextElementSibling.firstElementChild.textContent;
            }
        })

        const jsonData = {
            quantity: bags.value,
            categories: checkCategories,
            receiver: organization,
            address: adress.value,
            city: city.value,
            zip_code: code.value,
            phone_number: phoneNumber.value,
            data: data.value,
            time: time.value,
            pick_up_coment: info.value
        }

        fetch('http://127.0.0.1:8000/donation/', {
            headers: {
                'Content-Type': 'application/json',
                'charset': 'UTF-8'
            },
            method: 'POST',
            body: JSON.stringify(jsonData),
            redirect: 'follow'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                window.location.href = 'http://127.0.0.1:8000/donation/success/';

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    })
}


const donationArchiveFunc = function () {
    //after click on the Archive button, js send this action to backend and refresh site//
    let table = document.querySelector(".donation-history").children[2].firstElementChild;
    let button = table.querySelector("button");
    let buttonRow = button.parentElement.parentElement;
    let jsonData = {
        is_active: 'True',
        institution_id: buttonRow.id
    }
    fetch('http://127.0.0.1:8000/profile/', {
        headers: {
            'Content-Type': 'application/json',
            'charset': 'UTF-8',
        },
        method: 'POST',
        body: JSON.stringify(jsonData),
        redirect: 'follow'
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.reload(true);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

const archiveMark = function () {
    //Archive donations has diffrent bg color//
    let archiveRow = document.querySelectorAll(".taken");
    archiveRow.forEach(row => {
        let cell = row.querySelectorAll("td");
        cell.forEach(el => {
            el.style.fontColor = '#008080';
            el.style.background = 'grey';
        })
    })
}


archiveMark()

const passwordWalidator = function () {
    //function check force of our password
    //password must be longer then 8 marks and have big and small letter, number and special mark
    //in password confirmation field function checks if passwords are the same
    //when passwords are incorrect function will turn off submit button
    const password1 = document.querySelector("input[name=password]");
    const password2 = document.querySelector("input[name=password2]");
    const submitButton = document.querySelector(".form-group--buttons").lastElementChild;
    const reg = new RegExp("^([^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$");

    const buttonDisactivated = function () {
        submitButton.addEventListener("click", e => {
            e.preventDefault();
        })
    }

    password1.addEventListener("keyup", () => {
        if (password1.value.length >= 8) {
            if (!reg.test(password1.value)) {
                password1.nextElementSibling.innerHTML = '';
            } else {
                password1.nextElementSibling.innerHTML = 'Has??o musi zawiera?? wielk?? i ma???? liter??, liczb?? i znak specjalny';
                password1.nextElementSibling.style.color = 'red';
                buttonDisactivated();
            }
        } else {
            password1.nextElementSibling.innerHTML = 'Has??o musi zawiera?? wielk?? i ma???? liter??, liczb?? i znak specjalny oraz mie?? minimum 8 znak??w';
            password1.nextElementSibling.style.color = 'red';
            buttonDisactivated();
        }
    })

    password2.addEventListener("keyup", () => {
        if (password2.value === null) {
            buttonDisactivated();
        }
        if (password1.value === password2.value) {
            password2.nextElementSibling.innerHTML = '';
        } else {
            password2.nextElementSibling.innerHTML = 'Has??a nie s?? takie same';
            password2.nextElementSibling.style.color = 'red';
            buttonDisactivated();
        }
    })
}

passwordWalidator()