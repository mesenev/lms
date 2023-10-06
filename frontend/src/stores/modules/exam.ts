import api from "@/stores/services/api";
import {defineStore} from "pinia";
import type {ExamModel} from "@/models/ExamModel";
import {computed, ref} from "vue";

export const useExamStore = defineStore('exam', () => {

    const examsByLesson = ref<Dictionary<ExamModel[]>>({});

    const currentExam = ref<ExamModel | null>(null);

    const newExam = computed(() => {
        return {
            id: NaN,
            name: '',
            lesson: NaN,
            description: '',
            questions: [],
            max_points: 0,
            test_mode: '',
            is_hidden: true,
        } as ExamModel;
    })

    async function fetchExamsByLessonId(id: number): Promise<ExamModel[]> {
        if (id in examsByLesson.value) {
            return examsByLesson.value[id];
        }
        let answer = {data: {}};
        await api.get('/api/exam/', {params: {lesson_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        const result = answer.data as Array<ExamModel>;
        setExams({[id]: result});
        return result;
    }

    async function fetchExamById(id: number): Promise<ExamModel> {
        let answer = {data: {}};
        await api.get(`/api/exam/${id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        return answer.data as ExamModel;
    }

    function changeCurrentExam(payload: ExamModel | null) {
        currentExam.value = payload;
    }

    function changeExamVisibility(test: ExamModel) {
        const curTest = examsByLesson.value[test.lesson].find(el => el.id === test.id);
        if (curTest != undefined) {
            curTest.is_hidden = test.is_hidden;
        }
    }

    function setExams(payload: Dictionary<ExamModel[]>) {
        examsByLesson.value = {...examsByLesson.value, ...payload};
    }

    async function patchExam(params: { is_hidden: boolean; id: number }) {
        let answer = {data: {}};
        await api.patch(`/api/exam/${params.id}/`, {...params})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        const result = answer.data as ExamModel;
        changeCurrentExam(result);
        changeExamVisibility(result);
        return result;
    }

    return {
        examsByLesson, currentExam, newExam, fetchExamsByLessonId, fetchExamById, changeCurrentExam,
        changeExamVisibility, setExams, patchExam
    }
})

export default useExamStore;