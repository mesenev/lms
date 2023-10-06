import api from '@/stores/services/api'
import {defineStore} from "pinia";
import {computed, ref} from "vue";
import type {ProblemModel} from "@/models/ProblemModel";
import type {CatsProblemModel} from "@/models/CatsProblemModel";

export const useProblemStore = defineStore('problem', () => {

    const problemsByLesson = ref<Dictionary<ProblemModel[]>>({});
    const catsProblems = ref<Array<{ id: CatsProblemModel }>>([]);
    const currentProblem = ref<ProblemModel | null>(null);

    const getNewProblem = computed(() => {
        return {
            id: NaN, lesson: NaN, type: 'CW', name: '', description: '',
            completed: false, manual: false, language: null, cats_material_url: '', cats_id: NaN,
            de_options: '', test_mode: ''
        };
    })

    function changeCurrentProblem(payload: ProblemModel | null) {
        currentProblem.value = payload;
    }

    function setProblems(payload: Dictionary<ProblemModel[]>) {
        problemsByLesson.value = {...problemsByLesson.value, ...payload};
    }

    async function fetchProblems(data: object) {
        //TODO: remove or fix (data here is set of fields to filter)
        await api.get('/api/problem/', {params: data})
            .then(response => {
                setProblems(response.data);
            })
            .catch(error => {
                console.log(error);
            })
    }

    async function fetchProblemById(problemId: number): Promise<ProblemModel> {
        let answer = {data: {}};
        await api.get(`/api/problem/${problemId}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        return answer.data as ProblemModel;
    }

    async function fetchCatsProblemById(catsId: number): Promise<CatsProblemModel> {
        let answer = {data: {}};
        await api.get(`/api/cats-problem-description/${catsId}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        return answer.data as CatsProblemModel;
    }

    async function fetchProblemsByLessonId(id: number): Promise<ProblemModel[]> {
        let answer = {data: {}};
        await api.get('/api/problem/', {params: {lesson_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        const result = answer.data as Array<ProblemModel>;
        setProblems({[id]: result})
        return result;
    }

    async function fetchProblemsForCourse(course_id: number): Promise<ProblemModel[]> {
        let answer = {data: {}};
        await api.get(`/api/problem/by-course/${course_id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        return answer.data as Array<ProblemModel>;
    }

    async function patchProblem(problem: ProblemModel) {
        return await api.patch(`/api/problem/${problem.id}/`, problem);
    }

    return {
        problemsByLesson, catsProblems, currentProblem, getNewProblem, changeCurrentProblem,
        setProblems, fetchProblems, fetchProblemById, fetchCatsProblemById, fetchProblemsByLessonId,
        fetchProblemsForCourse, patchProblem
    }
})

export default useProblemStore;
