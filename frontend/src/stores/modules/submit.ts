import api from '@/stores/services/api'
import {defineStore} from "pinia";
import {computed, ref} from "vue";
import type {SubmitModel} from "@/models/SubmitModel";
import type {PaginatedList} from "@/models/PaginatedList";

export const useSubmitStore = defineStore('submit', () => {
    const _submits = ref<SubmitModel[]>([]);

    const defaultSubmit = computed(() => {
        return {
            id: NaN, problem: {id: NaN, name: ''}, student: NaN, content: '',
            status: 'NP', created_at: '', lesson: NaN, de_id: '', cats_result: {},
        };
    })
    const submits = computed(() => {
        return _submits.value;
    })

    function setSubmits(submits: SubmitModel[]) {
        _submits.value = submits;
    }

    function addSubmitToArray(submit: SubmitModel) {
        _submits.value.push(submit);
        _submits.value = [..._submits.value];
    }

    function changeSubmitStatus(payload: { id: number; status: string }) {
        _submits.value.map((submit) => {
            if (submit.id === payload.id) {
                submit.status = payload.status;
            }
        })
        _submits.value = [..._submits.value];
    }

    async function fetchSubmitsByProblemAndUser(payload: { problemId: number; userId: number },
    ): Promise<Array<SubmitModel>> {
        let answer = {};
        await api.get('/api/submit/', {
            params: {
                problem: payload.problemId,
                user: payload.userId,
            },
        })
            .then(response => {
                setSubmits(response.data);
                answer = response.data;
            })
            .catch(error => {
                console.error(error);
            })
        return answer as Array<SubmitModel>;
    }

    async function fetchFirstFiveAW(course_id: number): Promise<SubmitModel[]> {
        let answer = {};
        await api.get(`/api/submit/five-aw/${course_id}/`)
            .then(response => {
                answer = response.data;
            })
            .catch(error => {
                console.error(error);
            });
        return answer as SubmitModel[];
    }

    async function fetchProblemStats(problem_id: number): Promise<SubmitModel[]> {
        let answer = {};
        await api.get(`/api/submit/problem-stats/${problem_id}/`)
            .then(response => {
                answer = response.data;
            })
            .catch(error => {
                console.error(error)
            });
        return answer as SubmitModel[];
    }

    async function fetchSubmitsByCourse(
        payload: {
            course_id: number;
            page?: number;
            page_size?: number;
            [key: string]: number | string | undefined;
        },
    ): Promise<PaginatedList<SubmitModel>> {
        let answer = {};
        await api.get('/api/submit/', {
            params: payload,
        })
            .then(response => {
                answer = response.data;
            })
            .catch(error => {
                console.error(error);
            })
        return answer as PaginatedList<SubmitModel>;
    }

    async function fetchSubmitById(id: number): Promise<SubmitModel> {
        const answer = submits.value.find(x => x.id === id);
        if (answer) {
            return answer;
        }
        let data = {};
        await api.get(`/api/submit/${id}/`)
            .then((response) => {
                addSubmitToArray(response.data);
                data = response.data
            })
            .catch(error => {
                console.error(error);
            })
        return data as SubmitModel;
    }

    async function fetchCatsResult(submitId: number) {
        let data = {};
        await api.get(`/api/submit/cats-result/${submitId}/`)
            .then(response => {
                data = response.data
            })
            .catch(error => {
                console.error(error);
            })
        return data as object;
    }

    async function fetchLastSubmit(payload: { user_id: number; problem_id: number }) {
        let answer = {data: {}};
        await api.get(`/api/submit/last-user-submit/${payload.user_id}/${payload.problem_id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            });
        return answer.data as SubmitModel;
    }

    return {
        defaultSubmit, submits, setSubmits, addSubmitToArray, fetchSubmitsByProblemAndUser, fetchFirstFiveAW,
        fetchProblemStats, fetchSubmitsByCourse, changeSubmitStatus, fetchSubmitById, fetchCatsResult, fetchLastSubmit
    }
})

export default useSubmitStore;
