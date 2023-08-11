import type { CourseModel } from "@/models/CourseModel";
import type { UserModel } from '@/models/UserModel';
import type { UserProgress } from '@/models/UserProgress';
import { useCourseStore } from "@/stores/modules/course";
import api from "@/stores/services/api";
import {ref, computed} from "vue";
import type { Ref } from 'vue';
import { defineStore } from "pinia";


const useUserStore = defineStore('user', ()=>{

    const courseModule = useCourseStore()

    const user: Ref<UserModel> = ref({
    id: -1,
    username: '',
    first_name: '',
    last_name: '',
    study_group: '',
    staff_for: [],
    avatar_url: '',
    thumbnail: '',
    email: '',
    cats_account: null
  })
  const currentCourseStudents: Ref<Dictionary<UserModel>> = ref({});
  const cachedStudents:  Ref<Dictionary<UserModel>> = ref({});

  function fetchStudentsMutation(data: Dictionary<UserModel> ) {
    currentCourseStudents.value = data;
  }

  function fetchCachedStudents(data: Dictionary<UserModel>) {
    cachedStudents.value = data;
  }

  function receiveUser(received_user: UserModel) {
    user.value = received_user
  }

  function addStaffToArray(courseId: number) {
    user.value.staff_for.push(courseId);
    user.value.staff_for = [...user.value.staff_for];
  }

  async function fetchStudentsByCourseId(courseId: number): Promise<Dictionary<UserModel>> {
    const course: CourseModel = await courseModule.fetchCourseById(courseId);
    const answer = (course.students as UserModel[]).reduce<Dictionary<UserModel>>(
      (previousValue, currentValue) => {
        previousValue[currentValue.id] = currentValue;
        return previousValue;
      }, {});
    fetchStudentsMutation({ ...currentCourseStudents, [courseId]: answer });
    return answer;
  }

  async function fetchStudentsProgressByLessonId(): Promise<Array<UserProgress>> {
    let data = {data: {}}
    await api.get('/api/lessonprogress/').then(response => data = response)
      .catch(error => {
        console.log(error);
      });
    return data.data as Array<UserProgress>;
  }

  async function fetchUserById(userId: number): Promise<UserModel> {
    let data = { data: {} }
    if (userId in this.currentCourseStudents)
      return this.currentCourseStudents[userId];
    if (userId in this.cachedStudents)
      return cachedStudents[userId];
    await api.get(`/api/users/${userId}/`).then(response => data = response)
      .catch(error => {
        console.log(error);
      });
    fetchCachedStudents({ ...cachedStudents, [userId]: data.data as UserModel });

    return data.data as UserModel;
  }

  async function fetchUserFromSession(): Promise<UserModel> {
    let data = { data: {}}
    await api.get('/api/sessionuser').then(response => data = response)
      .catch(error => {
        console.log(error);
      });
    return data.data as UserModel;
  }

  return { user, currentCourseStudents, cachedStudents, fetchStudentsMutation, fetchCachedStudents,
  receiveUser, addStaffToArray, fetchStudentsByCourseId, fetchStudentsProgressByLessonId,
      fetchUserById, fetchUserFromSession
  }

})

export default useUserStore