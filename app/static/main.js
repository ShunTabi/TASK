"use strict";
//定義
function getTime() {
    const now = new Date(),
        y = now.getFullYear(),
        m = now.getMonth() + 1,
        d = now.getDate();
    const date = `${y}-${m}-${d}`;
    return date;
}
function test() {
    // alert("成功しました。")
}
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
//VueRouter
const router = new VueRouter({
    routes: [
        {
            path: "/task",
            component: {
                template: "#task",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        box: [],
                        genreBox: [],
                        task: "",
                        prior: "選択してください",
                        genre: "選択してください",
                        data: "",
                        ONOFF: true,
                        Id: 0,
                        FORM: false,
                    }
                },
                methods: {
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.box = res.data.box
                            })
                            .catch(res => {
                                console.log(res);
                            });
                    },
                    axiosSELECT2: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT2");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.genreBox = res.data.box;
                                console.log(this.genre);
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        params.append("Id", tg);
                        alert(params);
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.task = res.data.box[0][0]
                                this.prior = res.data.box[0][1]
                                this.genre = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false;
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams()
                        params.append("task", this.task);
                        params.append("prior", this.prior);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "INSERT");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                test();
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("task", this.task);
                        params.append("prior", this.prior);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("Id", this.Id);
                        params.append("method", "UPDATE");
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                test();
                                this.ONOFF = true;
                                this.task = "";
                                this.prior = "選択してください";
                                this.genre = "選択してください";
                                this.date = getTime();
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/task/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.axiosSELECT1();
                    this.axiosSELECT2();
                    this.date = getTime();
                }
            }
        },
        {
            path: "/activity",
            component: {
                template: "#activity1",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        taskBox: [],
                        task1: "選択してください",
                        today: "",
                        next: "",
                        date: "",
                        ONOFF: true,
                        taskBox: [],
                        activityBox: [],
                        task2: "ALL",
                        FORM: false,
                    }
                },
                methods: {
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        axios.post(`http://localhost:8000/app/activity/${this.task2}/1`, params)//task//num
                            .then(res => {
                                this.activityBox = res.data.box;
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosSELECT2: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT2");
                        axios.post(`http://localhost:8000/app/activity/${this.task2}/1`, params)
                            .then(res => {
                                this.taskBox = res.data.box;
                            })
                            .catch(res => {
                                alert(res)
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        axios.post(`http://localhost:8000/app/activity/SELECT/${tg}`, params)
                            .then(res => {
                                this.task1 = res.data.box[0][0]
                                this.today = res.data.box[0][1]
                                this.next = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false
                            })
                            .catch(res => {
                                alert(res)
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("method", "INSERT");
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/INSERT/1", params)
                            .then(res => {
                                test();
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("method", "UPDATE");
                        params.append("Id", this.Id);
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/UPDATE/1", params)
                            .then(res => {
                                test();
                                this.task1 = "選択してください";
                                this.today = "";
                                this.next = "";
                                this.date = getTime();
                                this.ONOFF = true;
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/activity/DELETE/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.axiosSELECT1();
                    this.axiosSELECT2();
                    this.date = getTime();
                }
            },
        },
        {
            path: "/activity/:key",
            component: {
                template: "#activity2",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        activityBox: [],
                        task: "",
                        today: "",
                        next: "",
                        date: "",
                        ONOFF: true,
                        FORM: false,
                    }
                },
                methods: {
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        axios.post(`http://localhost:8000/app/activity/${this.$route.params.key}/1`, params)//task//num
                            .then(res => {
                                this.activityBox = res.data.box;
                                console.log(this.activityBox);
                            })
                            .catch(res => {
                                console.log(res);
                            });
                    },
                    axiosSELECT3: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("method", "SELECT3");
                        axios.post(`http://localhost:8000/app/activity/SELECT/${tg}`, params)
                            .then(res => {
                                this.task1 = res.data.box[0][0]
                                this.today = res.data.box[0][1]
                                this.next = res.data.box[0][2]
                                this.date = res.data.box[0][3]
                                this.ONOFF = false
                            })
                            .catch(res => {
                                alert(res)
                            });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("method", "INSERT");
                        params.append("task", this.task);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/INSERT/1", params)
                            .then(res => {
                                test();
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("method", "UPDATE");
                        params.append("Id", this.Id);
                        params.append("task", this.task1);
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/activity/UPDATE/1", params)
                            .then(res => {
                                test();
                                this.today = "";
                                this.next = "";
                                this.date = getTime();
                                this.ONOFF = true;
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/activity/DELETE/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.task = this.$route.params.key;
                    this.axiosSELECT1();
                    this.date = getTime();
                }
            }
        },
        {
            path: "/classification",
            component: {
                template: "#classification",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        date: "",
                        genre: "",
                        box: [],
                        ONOFF: true,
                        Id: 0,
                        FORM: false,
                    }
                },
                methods: {
                    axiosSELECT1: function () {
                        const params = new URLSearchParams();
                        params.append("method", "SELECT1");
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                // console.log(res.data.box);
                                this.box = res.data.box;
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosSELECT2: function (tg) {
                        this.Id = tg;
                        const params = new URLSearchParams();
                        params.append("Id", tg);
                        params.append("method", "SELECT2")
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                // console.log(res.data);
                                this.ONOFF = false;
                                this.genre = res.data.box[0][0];
                                this.date = res.data.box[0][1];
                            })
                            .catch(function (error) { alert(error) });
                    },
                    axiosINSERT: function () {
                        const params = new URLSearchParams();
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "INSERT");
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                test();
                                this.axiosSELECT1();
                            })
                            .catch(function (error) { alert(error) });
                    },
                    axiosUPDATE: function () {
                        const params = new URLSearchParams();
                        params.append("Id", this.Id);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        params.append("method", "UPDATE")
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                test();
                                this.ONOFF = true;
                                this.Id = 0;
                                this.genre = "";
                                this.date = getTime();
                                this.axiosSELECT1();
                            })
                            .catch(function (error) { alert(error) });
                    },
                    axiosDELETE: function (tg) {
                        const params = new URLSearchParams();
                        params.append("method", "DELETE");
                        params.append("Id", tg);
                        axios.post("http://localhost:8000/app/classification/1", params)
                            .then(res => {
                                this.axiosSELECT1();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    FC: function () {
                        this.FORM = !this.FORM;
                    }
                },
                created: function () {
                    this.date = getTime();
                    this.axiosSELECT1();
                }
            }
        },
        {
            path: "/error",
            component: {
                template: "#error",
                delimiters: ["[[", "]]"],
                methods: {
                },
            }
        },
    ]
})

const app = new Vue({
    el: "#app",
    router: router,
    created: function () {
    }
})