window.AppAjax = (function () {
    function loading(message) {
        if (window.layer && layer.load) {
            return layer.load(1, {
                shade: [0.12, '#fff'],
                content: message || 'Loading...'
            });
        }
        return null;
    }

    function closeLoading(index) {
        if (index !== null && index !== undefined && window.layer && layer.close) {
            layer.close(index);
        }
    }

    function fail(message) {
        const text = message || 'Request failed. Please try again later.';
        if (window.layer && layer.msg) {
            layer.msg(text, {icon: 2, time: 1800});
        } else {
            alert(text);
        }
    }

    function post(options) {
        let loadingIndex;
        return $.ajax({
            async: options.async === undefined ? true : options.async,
            type: 'post',
            url: options.url,
            dataType: options.dataType || 'json',
            data: options.data || {},
            beforeSend: function () {
                loadingIndex = loading(options.loadingText);
                if (typeof options.beforeSend === 'function') {
                    options.beforeSend();
                }
            },
            success: function (data) {
                if (typeof options.success === 'function') {
                    options.success(data);
                }
            },
            error: function () {
                fail(options.errorText);
                if (typeof options.error === 'function') {
                    options.error();
                }
            },
            complete: function () {
                closeLoading(loadingIndex);
                if (typeof options.complete === 'function') {
                    options.complete();
                }
            }
        });
    }

    return {
        post: post,
        loading: loading,
        closeLoading: closeLoading,
        fail: fail
    };
})();
