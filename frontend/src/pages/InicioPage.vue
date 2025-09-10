<template>
  <div>
    <div class="d-flex align-items-center mb-3">
      <h2 class="section-title mb-0 flex-grow-1">Pedidos Pendientes</h2>
      <h2 class="section-title mb-0 flex-grow-1"><span class="alt">Pedidos Por Recoger</span></h2>
    </div>

    <div class="card card-soft mb-3 p-4" v-for="(p, i) in pedidos" :key="i">
      <div class="row g-2 align-items-center">
        
        <div class="col-md-7">
          <div class="fw-semibold">Pedido de: {{ p.cliente }}</div>
          <div>Ubicación: {{ p.ubicacion }}</div>
          <div class="mt-2 text-muted small">{{ p.fecha }}</div>
          <div class="mt-2">
            <span class="fw-semibold">Estado:</span>
            <span class="badge" :class="p.pagado ? 'badge-success' : 'badge-danger'">
              {{ p.pagado ? 'Pagado' : 'Por Pagar' }}
            </span>
          </div>
        </div>

        <div class="col-md-3 small detalles-borde">
          <div class="row">
            <div class="col-4 fw-semibold">Cant.</div>
            <div class="col-8 fw-semibold">Detalle</div>
            <template v-for="(d, idx) in p.detalle" :key="idx">
              <div class="col-4">{{ d.cant }}</div>
              <div class="col-8">{{ d.item }}</div>
            </template>
          </div>
        </div>

        <div class="col-md-2 text-center">
          <button class="btn btn-green">
            Revisar
            <img src="@/assets/Revisar.png" alt="Revisar pedido">
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
const pedidos = [
  {
    cliente: 'Andrea Garnica',
    ubicacion: 'Urb. Del Valle #12',
    fecha: '14/09/2024',
    pagado: true,
    detalle: [
      { cant: 50, item: 'Mesas' },
      { cant: 600, item: 'Sillas' },
      { cant: 80, item: 'Manteles' },
      { cant: 100, item: 'Sobremanteles color celeste' },
      { cant: 50, item: 'Cajas de vasos largos 12u' },
      { cant: 50, item: 'Cajas de cervezas 24u' },
      { cant: 40, item: 'Juegos de mesitas' },
    ],
  },
  {
    cliente: 'Andrea Garnica',
    ubicacion: 'Urb. Del Valle #12',
    fecha: '14/09/2024',
    pagado: false,
    detalle: [
      { cant: 50, item: 'Mesas' },
      { cant: 600, item: 'Sillas' },
      { cant: 80, item: 'Manteles' },
      { cant: 100, item: 'Sobremanteles color celeste' },
    ],
  },
]
</script>

<style scoped>
.section-title {
  text-align: center;
}

.detalles-borde {
  border: 1px solid #e0e0e0; /* Color del borde */
  border-radius: 8px;          /* Bordes redondeados */
  padding: 12px;               /* Espacio interior */
}

.btn {
  background-color: #2ABB68;
  color: white;
  display: inline-flex;  /* Usamos flex para alinear */
  align-items: center;    /* Centra verticalmente el texto y la imagen */
  gap: 8px;               /* Espacio entre el texto y la imagen */
  padding: 5px 80px;
}

img {
  height: 22px; /* Un poco más pequeño para que encaje mejor */
}
.btn-green:hover {
  background-color: #24a05c; /* Un verde más oscuro */
  border-color: #24a05c;
  color: white; /* Nos aseguramos que el texto siga blanco */
}
</style>