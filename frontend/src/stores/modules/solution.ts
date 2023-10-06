import api from "@/stores/services/api";
import {defineStore} from "pinia";
import {computed, ref} from "vue";
import type {SolutionModel} from "@/models/SolutionModel";

export const useSolutionStore = defineStore('solution', () => {
  const _solutions = ref<SolutionModel[]>([]);

  const solutions = computed(() => {
    return _solutions.value;
  })

  const defaultSolution = computed(() => {
    return {
      id: NaN,
      exam: NaN,
      student: NaN,
      user_answers: [],
      solution_points: NaN,
      status: 'await',
      question_verdicts: {},
    };
  })

  function setSolutions(solutions: SolutionModel[]) {
    _solutions.value = solutions;
  }

  async function fetchSolutionsByExamAndUser(payload: { examId: number; userId: number }): Promise<SolutionModel[]> {
    let answer = {};
    await api.get('/api/solution/', {
      params: {
        exam: payload.examId,
        user: payload.userId,
      }
    }).then(response => {
      answer = response.data;
      setSolutions(response.data);
    }).catch(error => {
      console.log(error);
    });
    return answer as Array<SolutionModel>;
  }

  async function fetchSolutionsByExam(examId: number): Promise<SolutionModel[]> {
    let answer = {};
    await api.get('/api/solution/', {
      params: {
        exam: examId,
      }
    }).then(response => {
      answer = response.data;
      setSolutions(response.data);
    }).catch(error => {
      console.log(error);
    });
    return answer as Array<SolutionModel>;
  }

  async function fetchSolutionById(id: number): Promise<SolutionModel> {
    let answer = {};
    await api.get(`/api/solution/${id}/`).then(response => {
      answer = response.data;
    }).catch(error => {
      console.log(error);
      throw error;
    });
    return answer as SolutionModel;
  }

  return {
    solutions, defaultSolution, setSolutions, fetchSolutionsByExamAndUser, fetchSolutionsByExam, fetchSolutionById
  }
})

export default useSolutionStore;
