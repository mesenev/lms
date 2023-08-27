import {defineStore} from "pinia";
import {computed, ref} from "vue";
import type {QuestionModel} from "@/models/QuestionModel";

export const useQuestionStore = defineStore('question', () => {
    const questions = ref<Dictionary<QuestionModel[]>>({});

    const newQuestion = computed(() => {
        return {
            index: 0,
            text: '',
            description: '',
            answer_type: 'input',
            all_answers: [],
            correct_answers: [],
            attachment_url: '',
            points: 0,
        } as QuestionModel
    })

    function setQuestions(payload: Dictionary<QuestionModel[]>) {
        questions.value = {...questions.value, ...payload};
    }

    return {
        questions, newQuestion, setQuestions
    }
})

export default useQuestionStore;
