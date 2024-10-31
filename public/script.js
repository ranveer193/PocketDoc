const symptomsList = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills",
    "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting",
    "burning_micturition", "spotting_urination", "fatigue", "weight_gain", "anxiety",
    "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy",
    "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes",
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin",
    "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain",
    "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine",
    "yellowing_of_eyes", "acute_liver_failure", "fluid_overload", "swelling_of_stomach",
    "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm", "throat_irritation",
    "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs",
    "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool",
    "irritation_in_anus", "neck_pain", "dizziness", "cramps", "bruising", "obesity", "swollen_legs",
    "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails",
    "swollen_extremeties", "excessive_hunger", "drying_and_tingling_lips", "slurred_speech",
    "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck", "swelling_joints",
    "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness",
    "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine",
    "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_(typhos)",
    "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes"
];

const symptomInput = document.getElementById('symptom-input');
const dropdown = document.getElementById('symptoms-dropdown');
const selectedSymptomsContainer = document.getElementById('selected-symptoms');
const resultDiv = document.getElementById('result');
const resultDisease = document.getElementById('result-disease');
const resultMedicine = document.getElementById('result-medicine');
const submitBtn = document.getElementById('submit-btn');

let selectedSymptoms = [];

symptomInput.addEventListener('input', function () {
    const value = this.value.toLowerCase();
    dropdown.innerHTML = ''; // Clear previous results

    if (value) {
        const filteredSymptoms = symptomsList.filter(symptom => symptom.includes(value));
        if (filteredSymptoms.length) {
            dropdown.style.display = 'block'; // Show dropdown
            filteredSymptoms.forEach(symptom => {
                const div = document.createElement('div');
                div.classList.add('dropdown-item');
                div.textContent = symptom;
                div.onclick = function () {
                    addSymptom(symptom);
                };
                dropdown.appendChild(div);
            });
        } else {
            dropdown.style.display = 'none'; // Hide dropdown if no matches
        }
    } else {
        dropdown.style.display = 'none'; // Hide dropdown when input is empty
    }
});

function addSymptom(symptom) {
    if (!selectedSymptoms.includes(symptom)) {
        selectedSymptoms.push(symptom);
        const symptomBadge = document.createElement('span');
        symptomBadge.classList.add('symptom-badge');
        symptomBadge.textContent = symptom;

        const removeBtn = document.createElement('span');
        removeBtn.textContent = '✖';
        removeBtn.classList.add('remove-symptom');
        removeBtn.onclick = function () {
            selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
            symptomBadge.remove();
            if (!selectedSymptoms.length) {
                resultDiv.style.display = 'none'; // Hide result when no symptoms
            }
        };

        symptomBadge.appendChild(removeBtn);
        selectedSymptomsContainer.appendChild(symptomBadge);
        symptomInput.value = ''; // Clear input
        dropdown.style.display = 'none'; // Hide dropdown after selection
    }
}

// Submit button action
submitBtn.addEventListener('click', async function () {
    const resultDiv = document.getElementById('result');
    if (selectedSymptoms.length > 0) {
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symptoms: selectedSymptoms })
            });

            const data = await response.json();

            if (response.ok) {
                resultDisease.textContent = `Predicted Disease: ${data.Prediction}`;
                resultMedicine.textContent = `Medicine: ${data.Medicine}`;
                resultDiv.style.display = 'block'; // Show the result card
            } else {
                resultDiv.textContent = `Error: ${data.error || 'Unknown error occurred'}`;
            }
        } catch (error) {
            resultDiv.textContent = 'Error: Unable to submit symptoms.';
            console.error('Error:', error);
        }
    } else {
        resultDiv.textContent = 'No symptoms selected.';
    }
});