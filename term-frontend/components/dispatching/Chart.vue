<template>
  <canvas ref="myChart" />
</template>

<script setup lang="ts">
import Chart, { type ChartData, type ChartItem, type ChartOptions } from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import { ru } from 'date-fns/locale';

interface IChartData {
  x: Date,
  y: number
}

const props = defineProps({
  axYLabel: {
    type: String,
    default: 'Значение',
  },
  chartTitle: {
    type: String,
    default: 'Тепловая энергия',
  },
  chartValues: {
    type: Array as () => IChartData[],
    default: () => ([{ x: new Date(), y: 0 }]),
  },
});

const myChart = ref<ChartItem>();

const data: ChartData<'line', IChartData[]> = {
  datasets: [
    {
      label: props.chartTitle,
      borderColor: '#2D669F',
      backgroundColor: '#2D669F',
      fill: false,
      tension: 0.1,
      pointBorderWidth: 0,
      pointHoverRadius: 0,
      pointHoverBorderWidth: 0,
      pointRadius: 0,
      pointHitRadius: 0,
      data: props.chartValues,
    },
  ],
};

const options: ChartOptions<'line'> = {
  responsive: true,
  borderColor: 'gray',
  color: 'gray',
  interaction: {
    intersect: false,
  },
  scales: {
    x: {
      type: 'time',
      time: {
        tooltipFormat: 'dd MMM, HH:mm',
        unit: 'day',
      },
      adapters: {
        date: {
          locale: ru,
        },
      },
      display: true,
      title: {
        display: true,
      },
    },
    y: {
      display: true,
      title: {
        display: true,
        text: props.axYLabel,
      },
      suggestedMin: 0,
      suggestedMax: 90,
    },
  },
};

onMounted(() => {
  if (myChart.value) {
    // eslint-disable-next-line no-new
    new Chart(myChart.value, {
      type: 'line',
      data,
      options,
    });
  }
});
</script>

<style scoped>
.asd {
  color: #ffffffdd;
}
</style>
