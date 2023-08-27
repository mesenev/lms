import api from '@/stores/services/api'
import {defineStore} from "pinia";
import {computed, ref} from "vue";
import type {LessonModel} from "@/models/LessonModel";

export const useLessonStore = defineStore('lesson', () => {

    const currentLesson = ref<LessonModel | null>(null);
    const lessonsByCourse = ref<Dictionary<LessonModel[]>>({});

    const getNewLesson = computed(() => {
        return {
            id: NaN,
            course: NaN,
            name: '',
            description: '',
            lessonContent: '',
            problems: [],
            exams: [],
            materials: [],
            deadline: '2000-01-01',
            progress: [],
            scores: {},
            is_hidden: true,
        } as LessonModel;
    })

    function setLessons(payload: Dictionary<LessonModel[]>) {
        lessonsByCourse.value = {...lessonsByCourse.value, ...payload};
    }

    function changeCurrentLesson(payload: LessonModel | null) {
        currentLesson.value = payload;
    }

    function changeLessonVisibility(lesson: LessonModel) {
        const curLesson = lessonsByCourse.value[lesson.course].find(el => el.id === lesson.id);
        if (curLesson != undefined) {
            curLesson.is_hidden = lesson.is_hidden;
        }
    }

    async function deleteLesson(id: number) {
        await api.delete(`/api/lesson/${id}/`);
    }

    async function fetchLessonById(id: number): Promise<LessonModel> {
        let answer = {data: {}};
        await api.get(`/api/lesson/${id}/`)
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        return answer.data as LessonModel;
    }

    async function fetchLessonsByCourseId(id: number): Promise<LessonModel[]> {
        if (id in lessonsByCourse.value) {
            return lessonsByCourse.value[id];
        }

        let answer = {data: {}};
        await api.get('/api/lesson/', {params: {course_id: id}})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        const result = answer.data as Array<LessonModel>;
        setLessons({[id]: result})
        return result;
    }

    async function patchLesson(params: { is_hidden: boolean; id: number }) {
        let answer = {data: {}};
        await api.patch(`/api/lesson/${params.id}/`, {...params})
            .then(response => answer = response)
            .catch(error => {
                console.log(error);
            })
        const result = answer.data as LessonModel;
        changeCurrentLesson(result);
        changeLessonVisibility(result);
        return result;
    }

    return {
        currentLesson, lessonsByCourse, setLessons, changeCurrentLesson, changeLessonVisibility, deleteLesson,
        fetchLessonById, getNewLesson, fetchLessonsByCourseId, patchLesson
    }
})

export default useLessonStore;