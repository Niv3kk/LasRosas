<template>
  <div class="login-page">
    <div class="bg-image"></div>
    <div class="bg-overlay"></div>

    <div class="login-card card">
      <div class="card-body p-4 p-md-5 text-center">
        <img class="brand-logo mb-2" src="@/assets/Rosa.png" alt="Las Rosas" />
        <div class="brand-name mb-4">Las Rosas</div>

        <form @submit.prevent="onSubmit" novalidate class="text-start">
          <div class="mb-3">
            <label class="form-label">Usuario</label>
            <input v-model.trim="form.username" type="text"
                   class="form-control input-soft"
                   :class="{ 'is-invalid': errors.username }"
                   placeholder="Usuario" autocomplete="username" required />
            <div v-if="errors.username" class="field-hint invalid">{{ errors.username }}</div>
          </div>

          <div class="mb-4">
            <label class="form-label">Contraseña</label>
            <input v-model.trim="form.password" type="password"
                   class="form-control input-soft"
                   :class="{ 'is-invalid': errors.password }"
                   placeholder="Contraseña" autocomplete="current-password" required />
            <div v-if="errors.password" class="field-hint invalid">{{ errors.password }}</div>
          </div>

          <div v-if="errors._" class="alert-soft alert-soft-danger mb-3">{{ errors._ }}</div>

          <button class="btn btn-rose w-100" type="submit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Iniciar Sesión
          </button>
        </form>
      </div>
    </div>
  </div>    
</template>

<script setup>
import { reactive, ref } from 'vue'
// import { login } from '@/services/auth' // conecta luego

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '', _: '' })
const loading = ref(false)

function validate() {
  errors.username = form.username ? '' : 'El usuario es obligatorio'
  errors.password = form.password ? '' : 'La contraseña es obligatoria'
  return !errors.username && !errors.password
}

async function onSubmit() {
  errors._ = ''
  if (!validate()) return
  try {
    loading.value = true
    const data = await login({ username: form.username, password: form.password })
    // TODO: guarda usuario/token y redirige a dashboard
    console.log('LOGIN OK:', data)
    window.location.href = '/dashboard'
  } catch (e) {
    errors._ = e?.response?.data?.detail || 'Usuario o contraseña incorrectos.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===== Paleta ===== */
:root{
  --rose-btn: #C83647;
  --rose-btn-hover:#b63f45;
  --card-pink:#fbeeee;
  --input-gray:#dfe3e5;
}

/* ===== Layout Fullscreen ===== */
.login-page{
  position:relative;
  min-height:100vh;       /* con base.css ahora sí ocupa todo */
  width:100%;
  height: 100%;
  display:grid;
  place-items:center;
  overflow:hidden;
}

/* Fondo: foto + blur + cover */
.bg-image{
  position:absolute; inset:0;
  background:url('@/assets/ImagenDeFondo.jpg') center/cover no-repeat;
  filter: blur(8px);
  transform: scale(1.06);
  z-index:0;
}
/* Oscurecer */
.bg-overlay{
  position:absolute; inset:0;
  background: rgba(0,0,0,.40);   /* ajusta 0.35–0.5 */
  z-index:1;
}

/* ===== Tarjeta ===== */
.login-card{
  position:relative;
  width:min(92%, 520px);
  background:var(--card-pink);
  border:0;
  border-radius:16px;
  box-shadow:0 12px 36px rgba(0,0,0,.25);
  z-index:2;
  background-color: #FFFFFF;
}

/* Marca */
.brand-logo{ width:68px; height:68px; object-fit:contain; }
.brand-name{
  font-family:'Great Vibes', cursive;
  font-size:44px; line-height:1; color:#000;
}

/* ===== Inputs ===== */
.input-soft{
  background:var(--input-gray);
  border:0;
  height:48px;
  border-radius:10px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.35);
  background-color: #D9D9D9;
}
.input-soft::placeholder{ color:#6c757d; }

/* Mensaje bajo el campo (más sutil que invalid-feedback de BS) */
.field-hint{
  font-size:.875rem;
  margin-top:.25rem;
}
.field-hint.invalid{ color:#d9534f; } /* rojo suave */

/* ===== Botón ===== */
.btn-rose{
  background:var(--rose-btn);
  color:#fff;
  height:46px;
  border:0;
  border-radius:10px;
  font-weight:700;
  letter-spacing:.2px;
  background-color: #C83647;
}

/* Alert suave para error general */
.alert-soft{
  padding:.6rem .8rem;
  border-radius:10px;
  font-size:.95rem;
}
.alert-soft-danger{
  background:#fde2e4;
  color:#921a24;
}
.btn-rose:active,
.btn-rose:focus {
  background-color: #C83647 !important; 
  border-color: #C83647 !important;
  box-shadow: none !important;
}

/* ===== Responsive ===== */
@media (max-width: 420px){
  .brand-name{ font-size:36px; }
  .login-card{ border-radius:14px; }
}
</style>
