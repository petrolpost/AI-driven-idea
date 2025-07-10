document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#projectsTable tbody');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const maturityFilter = document.getElementById('maturityFilter');
    const langSwitchButton = document.getElementById('lang-switch');

    let projects = [];
    let sortColumn = null;
    let sortDirection = 'asc';
    let currentLang = 'zh';

    const translations = {
        en: {
            title: "Project Navigator",
            subtitle: "A dynamic, searchable list of all idea-based projects.",
            search_placeholder: "Search by name or description...",
            all_statuses: "All Statuses",
            all_maturities: "All Maturities",
            col_name: "Name",
            col_type: "Type",
            col_maturity: "Maturity",
            col_status: "Status",
            col_description: "Description",
            col_created: "Created",
            footer: "Powered by FastAPI & Vanilla JS.",
            data_load_error: "Failed to load data. Is the backend running?",
        },
        zh: {
            title: "项目导航",
            subtitle: "一个动态、可搜索的所有理念项目列表。",
            search_placeholder: "按名称或描述搜索...",
            all_statuses: "所有状态",
            all_maturities: "所有成熟度",
            col_name: "名称",
            col_type: "类型",
            col_maturity: "成熟度",
            col_status: "状态",
            col_description: "描述",
            col_created: "创建日期",
            footer: "由 FastAPI & Vanilla JS 强力驱动。",
            data_load_error: "数据加载失败。后端服务是否在运行？",
        }
    };

    function setLanguage(lang) {
        currentLang = lang;
        document.querySelectorAll('[data-lang-key]').forEach(element => {
            const key = element.getAttribute('data-lang-key');
            if (translations[lang] && translations[lang][key]) {
                if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                    element.placeholder = translations[lang][key];
                } else {
                    element.textContent = translations[lang][key];
                }
            }
        });
    }

    async function fetchProjects() {
        try {
            const response = await fetch('/api/projects');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            projects = await response.json();
            renderTable();
        } catch (error) {
            console.error("Could not fetch projects:", error);
            const errorMsg = translations[currentLang]?.data_load_error || translations.en.data_load_error;
            tableBody.innerHTML = `<tr><td colspan="6">${errorMsg}</td></tr>`;
        }
    }

    function renderTable() {
        const filteredProjects = projects
            .filter(p => {
                const searchLower = searchInput.value.toLowerCase();
                const statusFilterValue = statusFilter.value;
                const maturityFilterValue = maturityFilter.value;

                // Remove icon from filter value for correct matching
                const cleanStatusFilter = statusFilterValue.split(' ').pop();
                const cleanMaturityFilter = maturityFilterValue.split(' ').pop();

                return (
                    (p.name.toLowerCase().includes(searchLower) || p.description.toLowerCase().includes(searchLower)) &&
                    (cleanStatusFilter === '' || p.status === cleanStatusFilter) &&
                    (cleanMaturityFilter === '' || p.maturity === cleanMaturityFilter)
                );
            });
        
        if (sortColumn) {
            filteredProjects.sort((a, b) => {
                const valA = a[sortColumn];
                const valB = b[sortColumn];
                if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
                if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
                return 0;
            });
        }

        tableBody.innerHTML = filteredProjects.map(p => `
            <tr>
                <td><a href="/view/${p.readme_path}" target="_blank">${p.name}</a></td>
                <td>${p.project_type}</td>
                <td>${p.maturity}</td>
                <td>${p.status}</td>
                <td>${p.description}</td>
                <td>${p.created_date}</td>
            </tr>
        `).join('');
    }
    
    document.querySelectorAll('#projectsTable thead th').forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;
            if (sortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortDirection = 'asc';
            }
            renderTable();
        });
    });

    searchInput.addEventListener('input', renderTable);
    statusFilter.addEventListener('change', renderTable);
    maturityFilter.addEventListener('change', renderTable);

    langSwitchButton.addEventListener('click', () => {
        const newLang = currentLang === 'zh' ? 'en' : 'zh';
        setLanguage(newLang);
    });

    // Initial load
    setLanguage(currentLang);
    fetchProjects();
});
