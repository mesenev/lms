<template>
  <div class="course-generator">
    <div class="generator-card">
      <h2 class="title">Генератор курсов</h2>

      <div class="generator-form">
        <input
          id="courseName"
          v-model="courseName"
          type="text"
          class="input"
          placeholder="Например: Введение в Python, Основы маркетинга..."
          @keyup.enter="generateCourse"
        />

        <button
          @click="generateCourse"
          :disabled="!courseName.trim() || isLoading"
          class="generate-btn"
          :class="{ 'loading': isLoading }"
        >
          <span v-if="!isLoading">Сгенерировать курс</span>
          <span v-else>
            <span class="spinner"></span>
            Генерация...
          </span>
        </button>
      </div>

      <!-- Отображение ошибки -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/stores/services/api'
import { ref, watch } from 'vue'

// Реактивные данные
const courseName = ref('')
const isLoading = ref(false)
const error = ref(null)

// Валидация и ограничение длины названия
watch(courseName, (newVal) => {
  // Ограничиваем длину названия
  if (newVal.length > 100) {
    courseName.value = newVal.slice(0, 100)
  }
  // Очищаем ошибку при изменении ввода
  if (error.value) {
    error.value = null
  }
})

// Генерация курса
const generateCourse = async () => {
  // Валидация
  if (!courseName.value.trim()) {
    error.value = 'Пожалуйста, введите название курса'
    return
  }
  
  if (courseName.value.length < 3) {
    error.value = 'Название курса должно содержать минимум 3 символа'
    return
  }
  
  error.value = null
  isLoading.value = true
  
  try {
    await api.post('generate-course', {"courseName": courseName.value})   
  } catch (err) {
    error.value = 'Ошибка при генерации курса. Пожалуйста, попробуйте снова.'
    console.error('Generation error:', err)
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
.course-generator {
  width: min(100%, 64rem);
  min-height: 31rem;
  margin: 0 auto;
  padding: 1.4rem 2.1rem 10.75rem;
  border-radius: 8px;
  background: rgba(118, 118, 118, .34);
  box-shadow: 0 18px 40px rgba(0, 0, 0, .08);
  box-sizing: border-box;
  backdrop-filter: blur(2px);
}

.generator-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  text-align: center;
  color: #050505;
  margin: 0 0 1.45rem;
  font-size: 2rem;
  line-height: 1;
  font-weight: 900;
  letter-spacing: 0;
  text-transform: uppercase;
}

.generator-form {
  width: 100%;
  min-height: 13.8rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2.6rem;
  padding: 2rem 1.5rem;
  border-radius: 14px;
  background: rgba(255, 255, 255, .72);
  box-sizing: border-box;
}

.input {
  width: 100%;
  height: 2.65rem;
  padding: 0 1.25rem;
  border: 1px solid #8f8f8f;
  border-radius: 5px;
  background: rgba(255, 255, 255, .82);
  color: #202020;
  font-size: 1rem;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: #575757;
  box-shadow: 0 0 0 2px rgba(87, 87, 87, .14);
}

.input::placeholder {
  color: #c7c7c7;
}

.generate-btn {
  width: 14.7rem;
  min-height: 2.4rem;
  align-self: center;
  background: #8c8c8c;
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 3px;
  font-size: .95rem;
  font-weight: 700;
  cursor: pointer;
  transition: background .2s ease, transform .2s ease;
}

.generate-btn:hover:not(:disabled) {
  background: #737373;
}

.generate-btn:disabled {
  opacity: .62;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: #737373;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  width: 100%;
  max-width: 42rem;
  background: rgba(255, 232, 232, .9);
  color: #8f1f1f;
  padding: .75rem 1rem;
  border-radius: 5px;
  margin-top: 1rem;
}

@media (max-width: 640px) {
  .course-generator {
    padding: 1rem;
  }

  .generator-form {
    min-height: 11rem;
    gap: 1.5rem;
    padding: 1.25rem;
  }

  .title {
    font-size: 1.6rem;
  }

  .generate-btn {
    width: 100%;
  }

  .input {
    font-size: .9rem;
  }
}
</style>
