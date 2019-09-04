function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}


function loadUsers() {
  users_url = "/users"

  $("#user_id").prop("disabled", true);
  $('#user_id').select2(
    {placeholder: "Please wait..."}
  );

  $.getJSON(users_url, function (data) {
      $('#user_id').append("<option></option>");
      $.each(data, function (index, value) {
          $('#user_id').append('<option value="' + value.id + '">' + value.name + " (" + value.id + ")" + '</option>');
      });
      $("#user_id").prop("disabled", false);
      $('#user_id').select2(
        {placeholder: "User (ID)"}
      );
    });
}


function loadAutoPivots() {
  url = "/autopivots";
  var autopivotsEls = $(".autopivots");
  var userId = $("#user_id").val();

  autopivotsEls.prop("disabled", true);
  autopivotsEls.select2({placeholder: "Please wait..."});

  $.getJSON(url, function (data) {
      autopivotsEls.append("<option></option>");
      $.each(data, function (index, value) {autopivotsEls.append(
        '<option value="' + value.id + '">' + value.id + '</option>');});
      autopivotsEls.prop("disabled", false);
      autopivotsEls.select2({placeholder: "Select autopivots."});
    });
}


function loadAutoCohorts() {
  url = "/autocohorts";
  var autocohortsEls = $(".autocohorts");
  var userId = $("#user_id").val();

  autocohortsEls.prop("disabled", true);
  autocohortsEls.select2({placeholder: "Please wait..."});

  $.getJSON(url, function (data) {
      autocohortsEls.append("<option></option>");
      $.each(data, function (index, value) {autocohortsEls.append(
        '<option value="' + value.id + '">' + value.id + '</option>');});
      autocohortsEls.prop("disabled", false);
      autocohortsEls.select2({placeholder: "Select autocohorts."});
    });
}


function loadUsers() {
  users_url = "/users"

  $("#user_id").prop("disabled", true);
  $('#user_id').select2(
    {placeholder: "Please wait..."}
  );

  $.getJSON(users_url, function (data) {
      $('#user_id').append("<option></option>");
      $.each(data, function (index, value) {
          $('#user_id').append('<option value="' + value.id + '">' + value.name + " (" + value.id + ")" + '</option>');
      });
      $("#user_id").prop("disabled", false);
      $('#user_id').select2(
        {placeholder: "User (ID)"}
      );
    });
}


function getEntities(endpoint, extras) {
  var url = "https://silver-api.jampp.com/general/v1/";

  url = url + endpoint + '?';
  if(typeof extras !== "undefined") {
    Object.keys(extras).forEach(function(key) {
      url += key + '=' + extras[key].join(',');
    });
  }

  return fetch(url, {credentials: 'include'}).then(
    function(response) {
      if (response.status == 200) {
        return response.json();
      } else if (response.status == 401) {
        alert('You need to log into Silver to be able to use AutoPivot.');
      }
      return;
    }
  );
}


function loadFilterContent(elementId, endpoint, extras) {
  // Add options to selectors
  var entity = endpoint.split('?')[0];
  var element = $("#" + elementId);

  var name_attr = 'name';  // 'name' is not the name for some entities
  if (endpoint == 'sources') {
    name_attr = 'company';
  }

  element.empty();
  element.prop("disabled", true);
  element.select2({width: '70%', placeholder: "Please wait..."});

  promise = getEntities(endpoint, extras);
  promise.then(function(json) {
    var data = json.data;
    element.append("<option></option>");
    data.forEach(function(item, index) {
      element.append(
        '<option value="' + item.id + '">'  // Option value
        + item[name_attr] + " (" + item.id + ")"  // Option text
        + '</option>'
      );
    });
    element.prop("disabled", false);
    element.select2({
      width: '70%',
      placeholder: capitalize(endpoint) + " (ID)"
    });
  });
};


function showFilter(content) {
  var filterName = content.params.data.id;
  var filterToShow = document.getElementById('div_' + filterName);
  filterToShow.classList.add('active');

  var endpoints = {'source': 'sources', 'country': 'countries'};

  if (filterName in endpoints) {
    loadFilterContent(filterName, endpoints[filterName]);
  }
}


function hideFilter(content) {
  var filterName = content.params.data.id
  var filterToHide = document.getElementById('div_' + filterName);
  filterToHide.classList.remove('active');

  // Remove selection.
  $('#' + filterName).val(null).trigger('change');
}


function loadCohortEvents(){
  var applicationsEl = $('#application');
  var element = $('#value');
  var extras = {};

  var applications = applicationsEl.select2('data').map(
    function (x) {return x.id;});
  if (!(applications && applications.length)) {
    return;
  }
  extras['application_id'] = applications;
  element.prop("disabled", true);
  element.select2({placeholder: "Please wait..."});

  promise = getEntities('events', extras);
  promise.then(function(json) {
    var data = json.data;
    element.append("<option></option>");
    data.forEach(function(item, index) {
      element.append(
        '<option value="ev(' + item.id + ')">'  // Option value
        + item.token + " (" + item.id + ")"  // Option text
        + '</option>'
      );
    });
    element.prop("disabled", false);
    element.select2({
      placeholder: "Event (ID)"
    });
  });
}


function showCustomDaysCohort() {
  var chosen = $(this).val();
  if (chosen == '{}d') {
    $('#div_cohort_number_of_days').toggleClass('hidden');
  }
}


function loadSchedulingBlock() {
  $('.datepicker').datepicker({format: 'yyyy-mm-dd'});
  loadUsers();
  $('#active_filters').on('select2:select', showFilter);
  $('#active_filters').on('select2:unselect', hideFilter);
}


function loadCohortBlock() {
  $('#value').prop("disabled", true);
  $('#value').select2({width: "100%", placeholder: "Select an application."});

  $('#application').on('select2:select', loadCohortEvents);
  $('#application').on('select2:unselect', loadCohortEvents);

  $('#right_to').change(showCustomDaysCohort);
}


function loadChildContent(parentEl, parentName, childEl, endpoint) {
  childEl.empty();
  childEl.prop("disabled", true);
  childEl.select2({width: '70%', placeholder: "Please wait..."});

  var extras = {};
  var parentContent = parentEl.select2('data').map(
    function (x) {return x.id;});
  if (parentContent && parentContent.length) {
    extras[parentName + '_id'] = parentContent;
  } else {
    childEl.select2(
      {width: '70%', placeholder: "Select " + parentName + "s"}).trigger('change');
    return;
  }

  promise = getEntities(endpoint, extras);
  promise.then(function(json) {
    var data = json.data;
    childEl.append("<option></option>");
    data.forEach(function(item, index) {
      childEl.append(
        '<option value="' + item.id + '">'  // Option value
        + item.name + " (" + item.id + ")"  // Option text
        + '</option>'
      );
    });
    childEl.prop("disabled", false);
    childEl.select2({width: '70%', placeholder: capitalize(endpoint) + " (ID)"});
  });
  return;
}


function loadEntities() {
  var advertiserEl = $('#advertiser');
  var applicationEl = $('#application');
  var campaignEl = $('#campaign_group');
  var groupEl = $('#campaign');

  var entitiesLineage = ['advertiser', 'application', 'campaign_group', 'campaign'];

  advertiserEl.select2({width: '70%', placeholder: 'Select an Advertiser'});
  loadFilterContent('advertiser', 'advertisers');

  applicationEl.prop("disabled", true);
  applicationEl.select2({width: '70%', placeholder: "Select advertisers"});

  campaignEl.prop("disabled", true);
  campaignEl.select2({width: '70%', placeholder: "Select applications"});

  groupEl.prop("disabled", true);
  groupEl.select2({width: '70%', placeholder: "Select campaigns"});

  advertiserEl.on('change', function () {
    loadChildContent(advertiserEl, 'advertiser', applicationEl, 'applications')
  });

  applicationEl.on('change', function () {
    loadChildContent(applicationEl, 'application', campaignEl, 'campaigns')
  });

  campaignEl.on('change', function () {
    loadChildContent(campaignEl, 'campaign', groupEl, 'groups')
  });
}


function loadFilters() {
  loadEntities();
}


function loadSpecialSeriesEvents(){
  var advertisersEl = $('#advertiser');
  var element = $('#event_id');
  var extras = {};

  element.empty();
  element.prop("disabled", true);
  element.select2({width: '70%', placeholder: "Please wait..."});

  var advertisers = advertisersEl.select2('data').map(
    function (x) {return x.id;});
  if (!(advertisers && advertisers.length)) {
    return;
  }
  extras['advertiser_id'] = advertisers;

  promise = getEntities('events', extras);
  promise.then(function(json) {
    var data = json.data;
    var array = [];
    data.forEach(function(item, index) {
      array.push(
        '<option value="' + item.id + '">'  // Option value
        + item.token + " (" + item.id + ")"  // Option text
        + '</option>'
      );
    });
    const distinct = [...new Set(array)]
    element.append("<option></option>");
    distinct.forEach(function(item, index) {element.append(item);});
    element.prop("disabled", false);
    element.select2({placeholder: "Event (ID)"});
  });
}
