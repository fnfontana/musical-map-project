### Como transformar o **index.html** num dashboard realmente vivo, que captura tudo direto do GitHub

A sua página já está bem-estruturada e bonita; o que falta é trocar os números “de mentirinha” por dados que venham da API do GitHub e criar uma esteira automática para que isso aconteça sem expor _tokens_ sensíveis.  
A seguir está um roteiro completo dividido em duas camadas:

| Camada | Quando usar | Resumo da ideia |
|--------|-------------|-----------------|
| **A. Fetch direto no browser** | Projeto **100 % público** e poucas requisições (≤ 60/h). | JavaScript no próprio _index.html_ faz chamadas REST anônimas. |
| **B. Build/CI + JSON estático** | Projeto privado **ou** muitas requisições, ou se quiser esconder o token. | Um workflow do GitHub Actions roda a cada _push_ ou via `schedule:` e grava um `data.json`; o dashboard só lê esse arquivo. |

---

## 1. Mapeie seu trabalho dentro do GitHub

| Recurso GitHub | Como ele entra no dashboard |
|----------------|-----------------------------|
| **Issues**     | Cada issue é uma tarefa. Use rótulos (`labels`) para: componente (`autonomous`, `interface`, `refactor`, etc.) e status (`backlog`, `in-progress`, `completed`). |
| **Milestones** | Marcam as _sprints_ (Fundação, Automação, …). |  ([REST API endpoints for milestones - GitHub Docs](https://docs.github.com/en/rest/issues/milestones?utm_source=chatgpt.com)) |
| **Commits / Pull Requests** | Alimentam o gráfico de progresso real vs. planejado. |
| **Checks/Actions**          | Cobertura, qualidade, etc. podem vir de _badges_ ou da API de _commit statuses_.  ([REST API endpoints for commit statuses - GitHub Docs](https://docs.github.com/en/rest/commits/statuses?utm_source=chatgpt.com)) |

---

## 2. Camada A — Fetch direto no browser (rápido de testar)

1. **Adicione um script no final do body** (logo antes de `</script>` existente):

```html
<script>
const owner = 'fnfontana';
const repo  = 'musical-map-project';
const api   = `https://api.github.com/repos/${owner}/${repo}`;

async function getJSON(url){
  const r = await fetch(url, { headers:{ 'Accept':'application/vnd.github+json'} });
  return r.json();
}

/* 2. Issues ---------------------------------------------------------------*/
async function loadIssues(){
  const issues = await getJSON(`${api}/issues?state=all&per_page=100`); // inclui PRs → filtre
  const onlyIssues = issues.filter(i => !i.pull_request);
  /* Transforma em estrutura {status,component} */
  return onlyIssues.map(i => {
      const labels = i.labels.map(l=>l.name);
      const comp   = labels.find(l => ['autonomous','interface','refactor','data','monitoring'].includes(l)) || 'other';
      const status = labels.find(l => ['backlog','in-progress','completed'].includes(l)) || 
                     (i.state === 'closed' ? 'completed' : 'pending');
      return {title:i.title,component:comp,status:status,url:i.html_url};
  });
}

/* 3. Milestones (sprints) -------------------------------------------------*/
async function loadMilestones(){
   return getJSON(`${api}/milestones?state=all&per_page=10`);
}

/* 4. Commits para o gráfico ----------------------------------------------*/
async function commitsCount(){
   const commits = await getJSON(`${api}/commits?per_page=100`);
   return commits.length;  // exemplo simples
}

(async ()=>{
   const tasks = await loadIssues();
   const sprints = await loadMilestones();
   /* --- Atualize contadores e Kanban --- */
   renderTasks(tasks);
   renderSprints(sprints);
   /* --- Atualize Chart.js --- */
   updateCharts(tasks,sprints);
   document.getElementById('last-update').textContent = new Date().toLocaleString('pt-BR');
})();
</script>
```

2. **Substitua** os números hard-coded (25, 11, etc.) por funções que contam `tasks.filter(t=>t.status==='completed').length` e afins.

3. **Remova** quaisquer valores fixos em seus datasets do Chart.js e preencha dinamicamente (por exemplo `data: planned.map(p=>p.percent)`).

4. **Hospede o dashboard** (GitHub Pages, Netlify, Vercel). Só funciona via HTTPS ou em `localhost` (CORS).

Limites:

* API anônima = 60 requisições/h.  
* Todo mundo verá seus números em tempo real, mas o token não é exposto.

---

## 3. Camada B — Workflow que gera `data.json` (recomendado p/ produção)

**.github/workflows/build-dashboard.yml**

```yaml
name: build-dashboard-data
on:
  push:
    branches: [ main ]
  schedule:
    - cron:  '0 * * * *'   # a cada hora ([Events that trigger workflows - GitHub Docs](https://docs.github.com/actions/learn-github-actions/events-that-trigger-workflows))
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Collect dashboard data
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        pip install ghapi
        python project/dashboard/scripts/collect.py > project/dashboard/data.json
    - name: Commit & Push data.json
      run: |
        git config --global user.email "bot@users.noreply.github.com"
        git config --global user.name  "dashboard-bot"
        git add project/dashboard/data.json
        git commit -m "chore: update dashboard data [skip ci]" || echo "no changes"
        git push
```

* `project/dashboard/scripts/collect.py` usa a biblioteca `ghapi` para ler issues, milestones e commits, consolida tudo e grava em **project/dashboard/data.json**.  
* Atualize seu `requirements.txt` com `ghapi>=3.1.0` para suportar o script.  
* No `index.html`, substitua o fetch direto na API por:

```js
fetch('data.json').then(r=>r.json()).then(data=>{
  const { issues, milestones, commitsCount } = data;
  renderTasks(issues);
  renderSprints(milestones);
  updateCharts(issues, milestones, commitsCount);
  document.getElementById('last-update').textContent = new Date().toLocaleString('pt-BR');
});
```

* Como o token fica só dentro do runner, não há risco de vazamento.  

---

## 4. Dicas rápidas de implementação

| Ação | Dica |
|------|------|
| **Definir componentes/status** | Crie _labels_ exatos (`autonomous`, `interface`, …) e aplique-os às issues. |
| **Atualizar gráficos** | Chart.js permite `chart.data.datasets[0].data = newData; chart.update();` dentro do seu `renderTasks()`. |
| **Cobertura / qualidade** | Use _badges_ do Codecov, Sonar ou `GET /repos/:owner/:repo/actions/runs` e calcule porcentagens. |
| **Deploy** | Ative GitHub Pages na branch `gh-pages` ou use Netlify; configure o workflow para fazer build e push. |
| **Paginação** | Se exceder 100 issues ou commits, leia o header `link` e faça novas requisições. |
| **GraphQL** | Para reduzir requisições, um único _GraphQL_ query traz issues+milestones+PRs de uma vez. |

---

## 5. Próximos passos sugeridos

1. **Padronize labels / milestones** no repositório agora mesmo.  
2. Escolha a camada (A ou B) e faça um _commit_ com o JavaScript de fetch.  
3. No próprio dashboard, mostre erros de API (e.g. falta de rate-limit) num `toast` discreto.  
4. Depois de estável, migre para a Camada B para escalar com segurança.

Com isso o seu dashboard passa a ser **autossuficiente**, refletindo automaticamente o que acontece no GitHub e economizando o seu tempo para focar no código, não na atualização manual. Boa implementação!
