import type { CourseModel } from "@/models/CourseModel";
import type { CourseScheduleModel } from "@/models/ScheduleModel";
import { ref, computed } from 'vue';
import type { Ref } from 'vue';
import { defineStore } from 'pinia'
import api from '@/stores/services/api'
import useUserStore from "@/stores/modules/user";


export const useCourseStore = defineStore('course', () => {

    const userStore = useUserStore()

    const currentCourse: Ref<CourseModel | null> = ref(null);
    const courses: Ref<Array<CourseModel>> = ref([]);

    const is_staff = computed( ()=>{
        if (!this.currentCourse)
            return false;
        return userStore.user.staff_for.includes(this.currentCourse.id);
    });

    const newCourse = computed(() =>{
        return {
            id: NaN, name: '', author: userStore.user, cats_id: null, lessons: [],
      completed: false, description: '', students: [], schedule: null, de_options: "",
        }
    });

    function setCourses(payload: Array<CourseModel>) {
        courses.value = payload;
    }

    function changeCurrentCourse(payload: CourseModel | null) {
        currentCourse.value = payload;
    }

    async function fetchUserCourses() {
        await api.get('/api/course/user_courses/')
        .then(response => {
            setCourses(response.data);
        })
        .catch(error => {
            console.log(error);
        })
    }

    async function fetchCourseById(id: number): Promise<CourseModel> {
        let answer = { data: {} };
        await api.get(`/api/course/${id}/`)
        .then(response => answer = response)
        .catch(error => {
            console.log(error);
        })
        return answer.data as CourseModel;
    }

    function addCourseToArray(element: CourseModel) {
        courses.value.push(element);
        courses.value = [...this.courses];
    }

    async function fetchCourseScheduleByCourseId(id: number): Promise<CourseScheduleModel> {
        let answer = { data: {} };
        await api.get(`/api/course-schedule/by-course/${id}/`)
        .then(response => answer = response)
        .catch(error => {
            console.log(error);
        })
        return answer.data as CourseScheduleModel;
    }

    return { currentCourse, courses, is_staff, newCourse, setCourses, changeCurrentCourse,
    fetchUserCourses, fetchCourseById, addCourseToArray, fetchCourseScheduleByCourseId }
})
