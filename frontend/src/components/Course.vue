<template>
  <div>
    CourseModel component
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { getModule } from 'vuex-module-decorators';
import Counter2 from '@/store/main';
import CourseModel from '@/models/CourseModel';
import router from '@/router';

export default defineComponent({
  name: 'Course',
  setup() {
    const MyModuleInstance = getModule(Counter2);
    const note = computed(() => store.state.currentNote);

    const saveNote = () => {
      store.dispatch('saveNote');
      router.push('/');
    };
    const DeleteNote = () => {
      store.commit('deleteNote', note);
      router.push('/');
    };

    const { currentRoute } = router;
    const fetchNote = () => {
      if (currentRoute.value.params.id) {
        const routeId: number = +currentRoute.value.params.id;
        store.dispatch('fetchCurrentNote', routeId);
      } else {
        const id = store.getters.getIdOfLastNote + 1;
        store.commit('setCurrentNote', {
          title: '',
          todos: [] as ToDo[],
          id,
        });
      }
    };
    onMounted(fetchNote);

    const updateTitle = (e: { target: { value: string } }) => {
      store.commit('updateTitle', e.target.value);
    };

    const addNewTodo = () => {
      store.commit('addNewTodo');
    };

    const onRemoveTodo = (index: number) => {
      store.commit('deleteTodo', index);
    };
    const onUpdateTodo = (text: string, index: number) => {
      const todos = [...store.state.currentNote.todos];

      todos[index] = { ...todos[index], text };
      store.commit('updateTodos', todos);
    };
    const onCheckboxClick = (completed: boolean, index: number) => {
      const todos = [...store.state.currentNote.todos];

      todos[index] = { ...todos[index], completed };
      store.commit('updateTodos', todos);
    };

    const cancelEdit = () => {
      // undo changes
      router.push('/');
    };
    const clearNote = () => {
      const id = store.getters.getIdOfLastNote + 1;
      store.commit('setCurrentNote', {
        title: '',
        todos: [] as ToDo[],
        id,
      } as Note);
    };

    return {
      note,
      saveNote,
      addNewTodo,
      cancelEdit,
      onRemoveTodo,
      onUpdateTodo,
      DeleteNote,
      clearNote,
      updateTitle,
      onCheckboxClick,
    };
  },
  beforeRouteLeave(to, from, next) {
    this.clearNote();
    next();
  },
});
</script>

<style>
.new-todo {
  display: flex;
  justify-content: flex-start;
  background-color: #e2e2e2;
  height: 36px;
  margin: 5px 0px;
  padding-top: 4px;
  padding-left: 10px;
  padding-right: 15px;
  border-radius: 5px;
}
</style>
