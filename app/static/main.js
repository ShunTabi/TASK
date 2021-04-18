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
    alert("成功しました。")
}
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
//VueRouter
const router = new VueRouter({
    routes: [
        {
            path: "/task1",
            component: {
                template: "#task1",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        box: [],
                    }
                },
                methods: {
                    axiosSelect: function () {
                        axios.post("http://localhost:8000/app/taskSelect/1")
                            .then(res => {
                                this.box = res.data.box
                            })
                            .catch(res => {
                                console.log(res);
                            });
                    },
                },
                created: function () {
                    this.axiosSelect();
                }
            }
        },
        {
            path: "/task2",
            component: {
                template: "#task2",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        genreBox: [],
                        task: "",
                        prior: "選択してください",
                        genre: "選択してください",
                        data: "",
                    }
                },
                methods: {
                    axiosInsert: function () {
                        const params = new URLSearchParams()
                        params.append("task", this.task);
                        params.append("prior", this.prior);
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/taskInsert", params)
                            .then(res => {
                                test();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosSelect: function () {
                        axios.post("http://localhost:8000/app/classificationNameSelect")
                            .then(res => {
                                this.genreBox = res.data.box;
                                console.log(this.genre);
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                },
                created: function () {
                    this.axiosSelect();
                    this.date = getTime();
                }
            }
        },
        {
            path: "/activity1",
            component: {
                template: "#activity1",
                delimiters: ["[[", "]]"],
                data: function () {
                    return {
                        taskBox: [],
                        activityBox:[],
                    }
                },
                methods: {
                    axiosSelect2: function () {
                        axios.post("http://localhost:8000/app/taskNameSelect2")
                            .then(res => {
                                this.taskBox = res.data.box
                            })
                            .catch(res => {
                                alert(res)
                            });
                    },
                    axiosSelect1: function () {
                        axios.post(`http://localhost:8000/app/activitySelect1`)
                            .then(res => {
                                this.activityBox = res.data.box;
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                },
                created: function () {
                    this.axiosSelect1();
                    this.axiosSelect2();
                }
            }
        },
        {
            path: "/activity2/:key",
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
                    }
                },
                methods: {
                    axiosSelect: function () {
                        axios.post(`http://localhost:8000/app/taskNameSelect/${this.$route.params.key}`)
                            .then(res => {
                                this.task = res.data.box[0][0];
                            })
                            .catch(res => {
                                console.log(res);
                            });
                    },
                    axiosSelect2: function () {
                        axios.post(`http://localhost:8000/app/activitySelect2/${this.$route.params.key}`)
                            .then(res => {
                                this.activityBox = res.data.box;
                                console.log(this.activityBox);
                            })
                            .catch(res => {
                                console.log(res);
                            });
                    },
                    axiosInsert: function () {
                        const params = new URLSearchParams();
                        params.append("today", this.today);
                        params.append("next", this.next);
                        params.append("date", this.date);
                        axios.post(`http://localhost:8000/app/activityInsert/${this.$route.params.key}`, params)
                            .then(res => {
                                test();
                                this.axiosSelect2();
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                },
                created: function () {
                    this.axiosSelect();
                    this.axiosSelect2();
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
                    }
                },
                methods: {
                    axiosSelect: function () {
                        axios.post("http://localhost:8000/app/classificationSelect/1")
                            .then(res => {
                                // alert(res.data.box);
                                this.box = res.data.box;
                            })
                            .catch(res => {
                                alert(res);
                            });
                    },
                    axiosInsert: function () {
                        const params = new URLSearchParams();
                        params.append("genre", this.genre);
                        params.append("date", this.date);
                        axios.post("http://localhost:8000/app/classificationInsert", params)
                            .then(res => {
                                test();
                                this.axiosSelect();
                            }).catch(function (error) { alert(error) });
                    },
                    axiosUpdate: function () { },//★★★
                    axiosDelete: function () { }//★★★
                },
                created: function () {
                    this.date = getTime();
                    this.axiosSelect();
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