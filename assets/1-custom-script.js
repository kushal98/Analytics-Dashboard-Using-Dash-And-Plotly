$(function () {
var colors = [
            { Name: "jQuery/HTML5/ASP.NET MVC Controls" },
            { Name: "ASP.NET Controls" },
            { Name: "Windows Forms Controls" },
            { Name: "WPF Controls" },
            { Name: "Android Native mobile controls" },
            { Name: "iOS Controls" },
            { Name: "SharePlus" },
            { Name: "ReportPlus" },
            { Name: "Indigo Studio" }
        ];

        $(function () {
            $("#multiSelectCombo").igCombo({
                width: 300,
                dataSource: colors,
                textKey: "Name",
                valueKey: "Name",
                multiSelection: {
                    enabled: true
                },
                dropDownOrientation: "bottom"
            });

            $("#checkboxSelectCombo").igCombo({
                width: 300,
                dataSource: colors,
                textKey: "Name",
                valueKey: "Name",
                multiSelection: {
                    enabled: true,
                    showCheckboxes: true
                },
                dropDownOrientation: "bottom"
            });

        });
});