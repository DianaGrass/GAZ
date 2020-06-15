const all_row = document.querySelectorAll('.row')
all_row.forEach((el)=>{
    let sum_for_all_quart = 0;
    el.querySelectorAll('.money').forEach((item)=>{
        sum_for_all_quart += Number(item.textContent);
    })
    const td = document.createElement('td');
    td.className = 'result-for_year'
    td.textContent = sum_for_all_quart
    el.append(td)
})