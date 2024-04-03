// contains a method that shows an html table containing a column for the table's column names and another columdn showing the value of each ot the table's columns for an element of the table with table.id=function_parameter  in the html element with id=detail_table, and a constructor that executes it
export class ReadController {
    id = window.id;  
    table = window.table;
    process = window.process;

    // replaces the contents of the html element with id=detail_table with an html table containing a column for the table's column names and another column showing the value of each of the table's columns for an element of the table with table.id=function_parameter
    constructor() {
        this.read(this.id);


    }

    // suppose there is a variable called table containing an array called columns with the table's column names
    // the parameter reg_id is the id of the element of the table that we want to read
  // to read the register, we need to call an axios http request to the endpoint: '/' + this.process.name + '/' + this.table.name + '/detail/{id}', { params: {} }
    read(reg_id) {
        let url = '/' + this.process.name + '/' + this.table.name + '/detail/' + reg_id;
        axios.get(url, { params: {} })
            .then((response) => {
                let data = response.data;
                let table = document.getElementById('detail_table');
                let html = '<table class="table table-striped table-bordered table-hover">';
                html += '<tr>';
                html += '<th>Column Name</th>';
                html += '<th>Value</th>';
                html += '</tr>';
                for (let i = 0; i < this.table.columns.length; i++) {
                    html += '<tr>';
                    html += '<td>' + this.table.columns[i] + '</td>';
                    html += '<td>' + data[this.table.columns[i]] + '</td>';
                    html += '</tr>';
                }
                html += '</table>';
                table.innerHTML = html;
            })
            .catch((error) => {
                console.log(error);
            });
    }  
}

